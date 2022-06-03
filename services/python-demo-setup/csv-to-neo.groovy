import org.apache.commons.io.IOUtils
import java.nio.charset.StandardCharsets
flowFile = session.get()
if(!flowFile) return  // bail if no flow file supplied

// write cypher query to file
def cypherLines = [
    "MATCH(n) RETURN COUNT(n)"
]
def cypherFile = new File("import_data.cypher")
cypherLines.each { line -> cypherFile.write(line) }

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
    cypherFile.delete()
}
