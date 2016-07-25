#python_distribute_lock_redis

（1）查看redis对应命令  
    http://redisdoc.com/
    http://redisdoc.com/string/setnx.html

（2）加锁注意TTL设定，否则无限等待

（3）释放锁需要pipe封装


c/c++版本实现可参考： 
http://git.oschina.net/clouduser/distribute_lock_redis
