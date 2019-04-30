import java.io.IOException;
import java.util.logging.*;
public class Main {

    public static class Test{
        void test(){
            Logger.getLogger("").info("Helloooo");
        }
    }
    public static void main(String argv[]){
        //This goes to the very beginning of main to ensure we clear the handlers and add the log.txt file handler.
        Logger rootLogger = Logger.getLogger("");
        for(var h : rootLogger.getHandlers()){
            rootLogger.removeHandler(h);
        }
        try {
            FileHandler hndlr = new FileHandler("log.txt");
            hndlr.setFormatter(new SimpleFormatter());
            rootLogger.addHandler(hndlr);
        }
        catch (IOException e){
            System.out.println(e.getMessage());
        }
        //Up until here must be in the beginning of the main function.

        //Now in any class in our program, we can simply call Logger.getLogger("") and then log an Info event. See class examples (Test and PacketHandler).
        rootLogger.info("Log msg here");
        new Test().test();


        PacketHandler ph = new PacketHandler();
        ph.sendPacket("how are you doing?".getBytes());
//        logger.removeHandler();


        CommonParser CP = new CommonParser();
        CP.Parse("Common.cfg");
    }
}
