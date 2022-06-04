import org.apache.commons.io.FileUtils
import java.nio.charset.StandardCharsets
flowFile = session.get()
if(!flowFile) return  // bail if no flow file supplied

def f = new File("ageoff.cypher")
f.text = "MATCH (n:User) WHERE n.createdAt < TIMESTAMP() - 24*60*60*1000 DETACH DELETE (n) RETURN COUNT(n) as number_of_deletes;"
try {
    def p = "cypher-shell --format plain --address ${neo4jUri.value} -f ageoff.cypher".execute()
    p.waitForOrKill(10000)
    if(p.exitValue())
        log.error(IOUtils.toString(p.getErr(), StandardCharsets.UTF_8))
    log.info(p.text)
} catch (Exception e) {
    log.error("cypher processing threw exeception, probably killed - see logs")
    throw e
} finally {
    f.delete()
}
session.transfer(flowFile, REL_SUCCESS)
