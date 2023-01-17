# SQLBuilder

### A class to build SQL sentence with chain function 
```
res=Query('tableA').filters('name:EQ','张三').limit(10).filters('id:GE',1).select('distinct id','name').offset(1).filter('NAME:IN',('张三','李四')).order_by('id desc')
print(res)
```

output:
```
SELECT
     distinct id ,
     name
 FROM
     tableA
 WHERE
     name = '张三'  AND
     id >= 1  AND
     NAME in ('张三', '李四')
 ORDER BY
     id desc
 LIMIT
     10
 OFFSET
     1
 ```
