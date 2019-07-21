依赖
===

需要安装 requests ：

```
pip install requests
pip install pyquery
```

使用示例
=======

```python
from api import
a = SysuGraduatedAPIClient()
for code in [
    'photo',
    'joke',
    'discounts',
    'message',
    'enterprise'
]:
    print '----[[ %s ]]----' % code
    for it in a.data_iter(code):
        print it
        print
    print 'data for %s total: %s' % (code, a.count(code))
    print
```

