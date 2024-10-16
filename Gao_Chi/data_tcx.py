import xml.etree.ElementTree as ET


def parse_tcx(file_path):
    # 解析 TCX 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # TCX 文件的命名空间
    namespace = {
        'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
    }

    # 提取活动信息
    activities = root.findall('ns:Activities/ns:Activity', namespace)

    for activity in activities:
        activity_type = activity.attrib.get('Sport')
        for lap in activity.findall('ns:Lap', namespace):
            lap_start_time = lap.attrib.get('StartTime')
            print(f'活动类型: {activity_type}, 开始时间: {lap_start_time}')

            # 提取每一圈的信息
            for track in lap.findall('ns:Track', namespace):
                for trackpoint in track.findall('ns:Trackpoint', namespace):
                    time = trackpoint.find('ns:Time', namespace).text
                    distance = trackpoint.find('ns:DistanceMeters', namespace)
                    heart_rate = trackpoint.find('ns:HeartRateBpm/ns:Value', namespace)
                    if distance is not None:
                        distance = distance.text
                    if heart_rate is not None:
                        heart_rate = heart_rate.text

                    print(f'时间: {time}, 距离: {distance}米, 心率: {heart_rate} bpm')


if __name__ == '__main__':
    file_path = '深圳市_跑步20241012193450.tcx'  # 替换为你的 .tcx 文件路径
    parse_tcx(file_path)
