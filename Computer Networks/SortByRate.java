import java.util.Comparator;

class SortByRate implements Comparator<Connection> {
    public int compare(Connection a, Connection b) {
        if ( a.connectionDownloadRate < b.connectionDownloadRate ) return -1;
        else if ( a.connectionDownloadRate == b.connectionDownloadRate ) return 0;
        else return 1;
    }
}