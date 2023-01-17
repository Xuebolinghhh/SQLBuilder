# SQLBuilder

res=Query('tableA').filters('name:EQ','张三').limit(10).filters('id:GE',1).select('distinct id','name').offset(1).filter('NAME:IN',('张三','李四')).order_by('id desc')
print(res)
