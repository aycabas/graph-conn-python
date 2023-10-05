import asyncio
import configparser
import json
from graph import Graph

async def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    await greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Create External Connection')
        print('2. Create Schema')
        print('3. Get External Connection')
        print('4. List External Connections')
        print('5. Delete External Connection')
        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                print('Goodbye...')
            elif choice == 1:
                await create_external_connection(graph)
            elif choice == 2:
                await create_schema(graph)
            elif choice == 3:
                await get_external_connection(graph)
            elif choice == 4:
                await list_external_connections(graph)
            elif choice == 5:
                await delete_external_connection(graph)
            else:
                print('Invalid choice!\n')
        except Exception as ex:
            print('Error:', ex, '\n')

async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user:
        print('Hello,', user.display_name)
        # For Work/school accounts, email is in mail property
        # Personal accounts, email is in userPrincipalName
        print('Email:', user.mail or user.user_principal_name, '\n')

async def display_access_token(graph: Graph):
    token = await graph.get_user_token()
    print('User token:', token, '\n')

async def list_inbox(graph: Graph):
    message_page = await graph.get_inbox()
    if message_page and message_page.value:
        # Output each message's details
        for message in message_page.value:
            print('Message:', message.subject)
            if (
                message.from_ and
                message.from_.email_address
            ):
                print('  From:', message.from_.email_address.name or 'NONE')
            else:
                print('  From: NONE')
            print('  Status:', 'Read' if message.is_read else 'Unread')
            print('  Received:', message.received_date_time)

        # If @odata.nextLink is present
        more_available = message_page.odata_next_link is not None
        print('\nMore messages available?', more_available, '\n')

async def create_external_connection(graph: Graph):
    await graph.create_connection()

async def create_schema(graph: Graph):
    connectionId = input("Please enter the connection id: ")
    await graph.create_schema(connectionId)

async def get_external_connection(graph: Graph):
   connectionId = input("Please enter the connection id: ")
   await graph.get_connection(connectionId)

async def list_external_connections(graph: Graph):
   await graph.list_connections()

async def delete_external_connection(graph: Graph):
   connectionId = input("Please enter the connection id: ")
   await graph.delete_connection(connectionId)
   
# Run main
asyncio.run(main())