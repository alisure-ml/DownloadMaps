import re
import os
import math
import random
import urllib.request
from urllib import request
from alisuretool.Tools import Tools

agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1']


class DownMap(object):

    # 经纬度反算切片行列号 3857坐标系
    @staticmethod
    def deg2num(lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        x_tile = int((lon_deg + 180.0) / 360.0 * n)
        y_tile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return x_tile, y_tile

    # 下载图片
    @staticmethod
    def get_img(t_path, s_path, x, y, _id=0, _all=0):
        try:
            f = open(s_path, 'wb')
            req = urllib.request.Request(t_path)
            req.add_header('User-Agent', random.choice(agents))  # 换用随机的请求头
            pic = urllib.request.urlopen(req, timeout=60)

            f.write(pic.read())
            f.close()
            Tools.print("{}/{} {}/{}".format(_id, _all, x, y))
        except Exception:
            Tools.print("{}/{} {}/{} 下载失败,重试".format(_id, _all, x, y))
            pass
        pass

    def main(self, save_path, zoom=15, left_top_deg=[36.022968, 120.064056], right_bottom_deg=[35.894891, 120.344615]):
        save_path = Tools.new_dir(save_path)

        left_top = self.deg2num(left_top_deg[0], left_top_deg[1], zoom)  # 下载切片的左上角角点
        right_bottom = self.deg2num(right_bottom_deg[0], right_bottom_deg[1], zoom)  # 下载切片的右下角角点

        x_num = right_bottom[0] - left_top[0]
        y_num = right_bottom[1] - left_top[1]
        Tools.print("total image is {}".format(x_num * y_num))
        Tools.print("sum x:{} sum y:{} [{}, {}, {}, {}]".format(
            x_num, y_num, left_top[0], right_bottom[0], left_top[1], right_bottom[1]))

        _now = 0
        for x in range(left_top[0], right_bottom[0]):
            for y in range(left_top[1], right_bottom[1]):
                _now += 1
                tile_path = "http://www.google.cn/maps/vt?lyrs=s@815&gl=cn&x={}&y={}&z={}".format(x, y, zoom)
                self.get_img(tile_path, os.path.join(save_path, "{}-{}.png".format(x, y)), x, y, _now, x_num * y_num)
                pass
            pass

        pass

    pass


if __name__ == '__main__':
    """
    https://www.google.cn/maps/vt?lyrs=s@804&gl=cn&x=841538&y=418050&z=20
    """
    path = "D:\map_alisure"
    DownMap().main(save_path=path, zoom=20,
                   left_top_deg=[34.2400, 108.9200], right_bottom_deg=[34.2300, 108.930])
    Tools.print('完成')
    pass

