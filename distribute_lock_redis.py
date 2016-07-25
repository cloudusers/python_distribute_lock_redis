import redis
import time,datetime


def acquire_lock(conn, lockname, identifier, expire=10):
        if conn.setnx(lockname, identifier):
                conn.expire(lockname, expire)
                return identifier
        elif not conn.ttl(lockname):
                conn.expire(lockname, expire)

        return False

def release_lock(conn, lockname, identifier):
        pipe = conn.pipeline(True)
        while True:
                try:
                        pipe.watch(lockname)
                        if pipe.get(lockname) == identifier:
                                pipe.multi()
                                pipe.delete(lockname)
                                pipe.execute()
                                return True
                        pipe.unwatch()
                        break
                except redis.exceptions.WatchError:
                        pass

        # we lost the lock
        return False




conn = redis.Redis(host='localhost', port=6379, db=0)

#1 identifier
#2 False
#11 True
#22 False
#33 barx2
#44 True

ret = acquire_lock(conn, "lockname", "identifier", 3)
print "1",ret
ret = acquire_lock(conn, "lockname", "identifier", 3)
print "2",ret
ret = release_lock(conn, "lockname", "identifier")
print "11",ret
ret = release_lock(conn, "lockname", "identifier")
print "22",ret

ret = acquire_lock(conn, "footest", "bartest", 10)
print "33",ret
