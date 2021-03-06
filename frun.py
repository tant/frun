# Mở https://www.plotaroute.com/routeplanner tạo một đường mong muốn rồi tải về
# Sau đó dùng tool GPS Track Editor để chỉnh lại độ mịn của route, thêm point và chỉnh lại 
# Xóa element <metadata> và <name> trong file gpx đã tải về rồi đổi tên thành input.xml
# Set giờ bắt đầu chạy (theo giờ GMT) vào point đầu tiên của file
# chạy tool lấy được file output.xml
# Thay thế 'ns0:' thành khoảng trống
# Copy hết từ đầu tới hết metadata của file garmin qua
# Copy time của P0 vào metadata rồi sửa cho cùng format
# Cập nhật lại giờ các P cho đúng format 
# sửa lat và lon của P0 sao cho cùng format
# Copy extenstion của P1 vào P0
# đổi lại thành gpx và dùng tool mở ra lần cuối




#<?xml version="1.0" encoding="UTF-8"?>
#<gpx creator="Garmin Connect" version="1.1"
#  xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/11.xsd"
#  xmlns:ns3="http://www.garmin.com/xmlschemas/TrackPointExtension/v1"
#  xmlns="http://www.topografix.com/GPX/1/1"
#  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns2="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
#  <metadata>
#    <link href="connect.garmin.com">
#      <text>Garmin Connect</text>
#    </link>
#    <time>2019-09-19T13:27:51.000Z</time>
#  </metadata>
# <trk>
#    <name>Thanh Pho Ho Chi Minh - Easy Run</name>
#    <type>running</type>
#    <trkseg>

import xml.etree.ElementTree as ET
from geopy import distance
import math
import random
import datetime

tree = ET.parse('input.xml')
trkseg = tree.getroot()[0][0]



p0 = trkseg[0]
lat0 = p0.attrib['lat']
lon0 = p0.attrib['lon']
c0 = (lat0, lon0)
time0 = p0[1].text
i = 0

for p in trkseg:
    if i==0 : 
        i = i+1
        continue
    else:
        # Tính khoảng cách với tọa độ trước đơn vị ra met
        c1 = (p.attrib['lat'], p.attrib['lon'])
        dist = distance.distance(c0, c1).m
        # Tính thời gian hoàn thành khoảng cách trên
        #   Tính vận tốc trung bình theo pace.
        # EDIT
        min4km = 1.82 # số phút hoàn thành 1km
        #   Tính vận tốc theo đơn vị m/s
        velocity = 1000 / (min4km*60)
        #   Gia giảm ngẫu nhiên chút
        # 1m/s = 60m/m = 3600m/h = 3.6kmh
        # randrange không chấp nhận số thực nên chia xuống nhân lên với 1000 xong xíu chia xuống
        # EDIT
        vstart = -1000
        vend = +1000
        vstep = 200
        
        velocity = velocity + random.randrange(vstart,vend,vstep)/10000
        #   số giây 
        duration = round(dist / velocity , 1)
        
        # Cộng thời gian trước với thời gian hoàn thành để ra thời điểm hoàn thành
        dt0 = datetime.datetime.fromisoformat(time0[:-1])
        td = datetime.timedelta(seconds=duration)
        dt1 = dt0+td
        time1 = dt1.isoformat() + 'Z'
        # cập nhật lại thời điểm hoàn thành vào dữ liệu
        p[1].text= time1
        
        
        # Thêm dữ liệu mở rộng
        ext = ET.Element('extensions')
        tpe = ET.SubElement(ext, 'gpxtpx:TrackPointExtension')
        #  Nhiệt độ
        temp = ET.SubElement(tpe, 'gpxtpx:atemp')
        temp.text = '30'
        # Nhịp tim
        # EDIT: Range tim
        hr = ET.SubElement(tpe, 'gpxtpx:hr')
        hr.text = str(random.randint(167,179))
        # Cadence
        # EDIT: Range cadence
        cad = ET.SubElement(tpe, 'gpxtpx:cad')
        cad.text = str(random.randint(79,92))
        p.append(ext)
        # độ thêm mức chính xác của tọa độ
        for j in range(23):
            p.attrib['lat'] = p.attrib['lat'] + str(random.randint(0,9))
            p.attrib['lon'] = p.attrib['lon'] + str(random.randint(0,9))
        # cập nhật lại dữ liệu mới
        c0 = c1
        time0 = time1
        i = i + 1

tree.write('output.xml')

