'''
Number（数字）
Python3 支持 int、float、bool、complex（复数）。

在Python 3里，只有一种整数类型 int，表示为长整型，没有 python2 中的 Long。

像大多数语言一样，数值类型的赋值和计算都是很直观的。

内置的 type() 函数可以用来查询变量所指的对象类型。
'''

a, b, c, d = 20, 5.5, True, 4+3j

print(type(a), type(b), type(c), type(d))

print(isinstance(a, int))
print(isinstance(c, bool))

'''
isinstance 和 type 的区别在于：

type()不会认为子类是一种父类类型。
isinstance()会认为子类是一种父类类型。
'''

# 注意：Python3 中，bool 是 int 的子类，True 和 False 可以和数字相加， True==1、False==0 会返回 True，但可以通过 is 来判断类型。

judge = issubclass(bool, int)
print('bool 是否是 int 的子类', judge)

# 当你指定一个值时，Number 对象就会被创建：
var1 = 1
var2 = 10
print(var1, var2)

'''
# 您也可以使用del语句删除一些对象引用。
# del语句的语法是：
del var1, var2
print(var1, var2)
'''

# 数值运算
print(5+4) # 加法
print(5-4) # 减法
print(5*4) # 乘法
print(5/4) # 除法，得到一个浮点数
print(5//4) # 除法，得到一个整数
print(5%4) # 取余
print(5**4) # 乘方

'''
1、Python可以同时为多个变量赋值，如a, b = 1, 2。
2、一个变量可以通过赋值指向不同类型的对象。
3、数值的除法包含两个运算符：/ 返回一个浮点数，// 返回一个整数。
4、在混合计算时，Python会把整型转换成为浮点数。
Python还支持复数，复数由实数部分和虚数部分构成，可以用a + bj,或者complex(a,b)表示， 复数的实部a和虚部b都是浮点型
'''

