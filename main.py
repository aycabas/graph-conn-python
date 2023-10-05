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

    user = await graph.get_user()
    print('Hello,', user.display_name)

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
                await graph.create_connection()
            elif choice == 2:
                connectionId = input("Please enter the connection id: ")
                await graph.create_schema(connectionId)
            elif choice == 3:
                connectionId = input("Please enter the connection id: ")
                await graph.get_connection(connectionId)
            elif choice == 4:
                await graph.list_connections()
            elif choice == 5:
                connectionId = input("Please enter the connection id: ")
                await graph.delete_connection(connectionId)
            else:
                print('Invalid choice!\n')
        except Exception as ex:
            print('Error:', ex, '\n')

# Run main
asyncio.run(main())