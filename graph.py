from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder)
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import (
    SendMailPostRequestBody)
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection
from msgraph.generated.models.external_connectors.schema  import Schema
from msgraph.generated.models.external_connectors.property_  import Property_
from kiota_abstractions.method import Method
from msgraph.graph_request_adapter import GraphRequestAdapter
import json

class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphServiceClient(self.device_code_credential, graph_scopes)

    async def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token

    async def get_user(self):
        # Only request specific properties using $select
        query_params = UserItemRequestBuilder.UserItemRequestBuilderGetQueryParameters(
            select=['displayName', 'mail', 'userPrincipalName']
        )

        request_config = UserItemRequestBuilder.UserItemRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        user = await self.user_client.me.get(request_configuration=request_config)
        return user
    
    async def get_inbox(self):
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            # Only request specific properties
            select=['from', 'isRead', 'receivedDateTime', 'subject'],
            # Get at most 25 results
            top=25,
            # Sort by received time, newest first
            orderby=['receivedDateTime DESC']
        )
        request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters= query_params
        )

        messages = await self.user_client.me.mail_folders.by_mail_folder_id('inbox').messages.get(
                request_configuration=request_config)
        return messages
    
    async def send_mail(self, subject: str, body: str, recipient: str):
        message = Message()
        message.subject = subject

        message.body = ItemBody()
        message.body.content_type = BodyType.Text
        message.body.content = body

        to_recipient = Recipient()
        to_recipient.email_address = EmailAddress()
        to_recipient.email_address.address = recipient
        message.to_recipients = []
        message.to_recipients.append(to_recipient)

        request_body = SendMailPostRequestBody()
        request_body.message = message

        await self.user_client.me.send_mail.post(body=request_body)


    async def create_connection(self):
        # create prompt for user to enter connection details
        connectionId = input("Enter Connection Id: ")
        connectionName = input("Enter Connection Name: ")
        connectionDescription = input("Enter Connection Description: ")

        new_connection = ExternalConnection(
            id=connectionId,
            name=connectionName,
            description=connectionDescription,
        )

        connection = await self.user_client.external.connections.post(body=new_connection)
        print ("Connection name:", connection.name)

    async def get_connection(self, connectionId: str):
        connection= await self.user_client.external.connections.by_external_connection_id(connectionId).get()
        print ("Connection name:", connection.name)

    async def list_connections(self):
        connections = await self.user_client.external.connections.get()
        for connection in connections.value:
            print("Connection name:", connection.name)

    async def delete_connection(self, connectionId: str):
        connectionId = input("Enter Connection Id to Delete: ")
        connection = await self.user_client.external.connections.by_external_connection_id(connectionId).delete()
        print ("Connection name:", connection.name)

    async def create_schema(self, connectionId: str):
        schema = Schema(
            base_type = "microsoft.graph.externalItem",
            properties = [
               Property_(
                name= str,
                type= str,
                is_searchable= True,
                is_retrievable= True,
                )
            ]
        )
        
        requestInfo = self.user_client.external.connections.by_external_connection_id(connectionId).schema.to_patch_request_information(body=schema)
        print ("RequestInfo:", requestInfo.content)
        requestMessage = await self.user_client.request_adapter.convert_to_native_async(requestInfo)
        requestMessage.http_method = Method.POST
        print ("RequestMessage:", requestMessage)
        res = await GraphRequestAdapter.send_async(self, requestMessage, schema, schema)
        print ("Schema:", res)
        #try:
         #   res = await self.user_client.external.connections.by_external_connection_id(connectionId).schema.patch(body=schema)
          #  print ("Schema:", res)
        #except Exception as e:
         #   print (e)
        #res = await self.user_client.external.connections.by_external_connection_id(connectionId).schema.patch(body=schema,request_configuration=None)
        #print ("Schema:", res)