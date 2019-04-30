import java.util.logging.Logger;

public class PacketHandler {
    Logger logger = Logger.getLogger("");
    //using logger as a class attribute (so that all the methods can use it).
    // Make sure it is initialized properly (either here since it is static or in constructor).


    PacketHandler(){
//        logger = Logger.getLogger(""); //get root logger
    }


    boolean sendPacket(byte[] msg_to_send){
        //send the msg on the correct socket

        logger.info("Hello Type Message:" + new String(msg_to_send) );
        return true;
    }
}
