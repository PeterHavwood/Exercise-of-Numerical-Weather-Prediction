# Net cdf 文件说明

通过print函数可以得到一个NC文件的基本结构：
```
dimensions(sizes): lon(144), lat(1), lev(17), time(12)

variables(dimensions): 
float64 lon(lon), 
float64 lat(lat), 
float64 lev(lev),
float64 time(time),
float32 uwnd(time, lev, lat, lon), 
float32 vwnd(time, lev, lat, lon), 
float32 hgt(time, lev, lat, lon), 
float32 air(time, lev, lat, lon)
```

可以把NC文件视作“多个”多维数组，在本例中有四个维度（dimensions）：经度lon、维度lat、高度（等压面）lev、时间。每一个多维数组存储一个变量（variables）的时空分布。变量的类型与C中类型一致，包括char、bit、shor、int、float、double（float64）。

注意，各维度本身也是一个变量，因此它们的信息由一个一维数组表示，如本例中的lon（lon）。第一个lon表示的是纬度变量（表示纬度具体的值），而第二个lon则代表lon维度（从0到len(lon)-1）。
