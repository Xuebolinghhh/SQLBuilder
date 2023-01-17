import textwrap
import functools

class Query:
    keywords = [
        'SELECT',
        'FROM',
        'WHERE',       
        'ORDER BY',
        'LIMIT',
        'OFFSET'
    ]

    def __init__(self,table_name):
        self.data = {k: [] for k in self.keywords}
        self.data['FROM'].append(_clean_up(table_name))
        self.data['SELECT'].append(_clean_up('*'))
    
    _condition_map = {'EQ':'=','GE':'>=','LE':'<=','NE':'!=','IN':'in','NIN':'not in','LIKE':'like'}

    def filters(self,condition,value):
        col = condition.split(':')[0]
        condition = condition.split(':')[1]
        if isinstance(value,int):
            self.data['WHERE'].append(_clean_up(str(col)+' '+self._condition_map[condition]+' '+str(value)))
        elif isinstance(value,(list,tuple)):
            value = tuple(value)
            self.data['WHERE'].append(_clean_up(str(col)+' '+self._condition_map[condition]+' '+str(value)))
        else:
            self.data['WHERE'].append(_clean_up(str(col)+' '+self._condition_map[condition]+' '+"'"+str(value)+"'"))
        # print(self.data['WHERE'])
        return self 

    def select(self,*args):
        self.data['SELECT']=[]
        for arg in args:
            self.data['SELECT'].append(_clean_up(str(arg)))
        return self

    def limit(self,value):
        self.data['LIMIT'].append(_clean_up(str(value)))
        return self 

    def offset(self,value):
        self.data['OFFSET'].append(_clean_up(str(value)))
        return self

    def order_by(self,value):
        if isinstance(value,str):
            element_list = value.split(' ')
            element_list = list(filter(lambda x:x !='',element_list))
            if len(element_list)==1:
                self.data['ORDER BY'].append(_clean_up(str(element_list[0])))
            elif len(element_list)==2:
                self.data['ORDER BY'].append(_clean_up(str(value)))
            else:
                raise SyntaxError('输入不符合规范')
        else:
            raise TypeError('输入不为字符串类型')

        return self

    # 定义SQL的输出部分
    def __str__(self):
        return ' '.join(self._lines())

    def _lines(self):
        for keyword, things in self.data.items():
            if not things:
                continue
            
            yield f'{keyword}\n'
            yield from self._lines_keyword(keyword,things)

    default_separator=','
    separators = dict(WHERE='AND')
    
    def _lines_keyword(self, keyword, things):
        for i, thing in enumerate(things, 1):
            last = i == len(things)

            yield self._indent(thing)

            if not last:
                try:
                    yield ' '+self.separators[keyword]
                except KeyError:
                    yield self.default_separator
            # if not last:
            #     yield self.default_separator

            yield '\n'
    
    _indent = functools.partial(textwrap.indent, prefix='    ')

def _clean_up(thing: str) -> str:
    return textwrap.dedent(thing.rstrip()).strip()

if __name__ == '__main__':
    res=Query('tableA').filters('name:EQ','张三').limit(10).filters('id:GE',1).select('distinct id','name').offset(1).filter('NAME:IN',('张三','李四')).order_by('id desc')
    print(res)