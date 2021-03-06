#include<stdio.h>
#include<sys/socket.h>
#include<errno.h>
#include<netdb.h>
#include<string.h>
#include<stdlib.h>
 
int main(int argc , char **argv)
{
    struct hostent *host;
    struct sockaddr_in sa;
    int err, 
        i,
        sock,
        start,
        end;
    char hostname[100];
     
    start = 1;
    end   = 1025; 

    if (argc != 2 ){
        printf("Usage: ./portscanner [hostname]\n");
        printf("Examples:\n");
        printf("\t./portscaner www.google.fr\n");
        printf("\t./portscaner 192.168.2.2\n");
        exit(3);
     }
    
    strncpy(hostname, argv[1], sizeof(hostname));
     
    strncpy((char*)&sa , "" , sizeof(sa));
    
    sa.sin_family = AF_INET;
     
    if(isdigit(hostname[0])){
        sa.sin_addr.s_addr = inet_addr(hostname);
    }
    else if( (host = gethostbyname(hostname)) != 0){
        strncpy((char*)&sa.sin_addr , (char*)host->h_addr , sizeof(sa.sin_addr));
    } else {
        herror(hostname);
        exit(2);
    }
     
    //Start the port scan loop
    printf("Starting scan [%d-%d]: \n", start, end);
    for( i = start ; i <= end ; i++) {
        sa.sin_port = htons(i);
        sock = socket(AF_INET , SOCK_STREAM , 0);
         
        if(sock < 0) {
            perror("\nSocket");
            exit(1);
        }
        err = connect(sock , (struct sockaddr*)&sa , sizeof sa);
         
        if( err < 0 ){
            fflush(stdout);
        } else {
            printf("%-5d open\n",  i);
        }
        close(sock);
    }
     
    printf("\r");
    fflush(stdout);
    return(0);
} 