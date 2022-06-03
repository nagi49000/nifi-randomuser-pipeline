import org.apache.commons.io.IOUtils
import org.apache.commons.io.FileUtils
import java.nio.charset.StandardCharsets
flowFile = session.get()
if(!flowFile) return  // bail if no flow file supplied

File csvFile = new File("import_me.csv")
FileUtils.copyInputStreamToFile(session.read(flowFile), csvFile)

// write cypher query to file
def cypherFile = new File("import_data.cypher")
cypherFile.text = """
CREATE CONSTRAINT user_login_uuid_unique IF NOT EXISTS ON (n:User) ASSERT n.loginUuid IS UNIQUE;
USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///import_me.csv' AS line
MERGE (u:User {loginUuid: line.login_uuid, nameFirst: line.name_first, nameLast: line.name_last})
RETURN COUNT(u);
"""

// neo4jUri specified as a property in the processor
def cypherShellCmd = "cypher-shell --format plain --address ${neo4jUri.value} -f import_data.cypher"

// run cypher-shell command, collecting fallout and messages for logging
try {
    def cypherProcess = cypherShellCmd.execute()
    cypherProcess.waitForOrKill(10000)  // int in millisecs
    if(cypherProcess.exitValue()) {
        log.error(IOUtils.toString(cypherProcess.getErr(), StandardCharsets.UTF_8))
        session.transfer(flowFile, REL_FAILURE)
    } else {
        log.warn(cypherProcess.text)
        session.transfer(flowFile, REL_SUCCESS)
    }
} catch (Exception e) {
    session.transfer(flowFile, REL_FAILURE)
    throw e
} finally {
    csvFile.delete()
    cypherFile.delete()
}
