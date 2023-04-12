
class WordDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver = driver

    def add(self, type, name, pl):
        # Define the Unit of Work
        def add_word(tx, type, name, pl):
            # Define the cypher statement
            cypher = f"MERGE (t:{type} " + """
            {name: $name, pl: $pl})
            RETURN t
            """

            # Run the statement within the transaction passed as the first argument
            result = tx.run(cypher, type=type, name=name, pl=pl)

            return result.single()

        with self.driver.session() as session:
            return session.execute_write(add_word, type, name, pl)

    def remove(self, name):
            # Define a transaction function to delete the HAS_FAVORITE relationship within a Write Transaction
        def remove_everything(tx, name):
            row = tx.run("""
                MATCH (m)
                WHERE m.name = $name
                DETACH DELETE m
            """, name=name)

            print(row)
            # If no rows are returnedm throw a NotFoundException
            if row == None:
                raise NotFoundException()

            return "success"

            # Execute the transaction function within a Write Transaction
        with self.driver.session() as session:
            # Return movie details and `favorite` property
            return session.execute_write(remove_everything, name)

    def all(self, type, sort, order, limit=6, skip=0):
        # Define the Unit of Work
        def get_movies(tx, type, sort, order, limit, skip):
            # Define the cypher statement
            cypher = f"MATCH (m:{type}) " + """
                WHERE m.`{0}` is not null
                RETURN m {{ .* }} AS noun
                ORDER BY m.`{0}` {1}
                SKIP $skip
                LIMIT $limit
            """.format(sort, order)

            # Run the statement within the transaction passed as the first argument
            result = tx.run(cypher, limit=limit, skip=skip)

            # Extract a list of Movies from the Result
            print("Words extracted")
            result_list = [row.value("noun") for row in result]
            return result_list

        with self.driver.session() as session:
            return session.execute_read(get_movies, type, sort, order, limit, skip)

    def create_relationship(self, node1_name, node2_name, relationship_name):
        def add_relationship(tx, node1_name, node2_name, relationship_name):
            result = tx.run(
                "MATCH (n1 {name: $node1_name}), (n2 {name: $node2_name}) "
                "MERGE (n1)-[r:" + relationship_name + "]->(n2) "
                "RETURN r",
                node1_name=node1_name, node2_name=node2_name
            )
            return result.single()["r"]
        with self.driver.session() as session:
            return session.execute_write(add_relationship, node1_name, node2_name, relationship_name)
