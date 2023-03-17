
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

            # Extract a list of Movies from the Result
            return result.single()

        with self.driver.session() as session:
            return session.execute_write(add_word, type, name, pl)

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
