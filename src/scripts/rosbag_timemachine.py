#!/usr/bin/env python3

#Merge two rosbags and if required sync the time

import sys
from SimplePyQtGUIKit import SimplePyQtGUIKit
from PyQt5 import QtGui, QtWidgets
import rosbag
import rospy
import subprocess
from optparse import OptionParser
from datetime import datetime


def bag_to_csv(options, fname):
    try:
        bag = rosbag.Bag(fname)
        bag_out = rosbag.Bag(fname.strip(".bag")+"_out.bag","w")
        streamdict = dict()
        stime = None
        if options.start_time:
            stime = rospy.Time(options.start_time)
        etime = None
        if options.end_time:
            etime = rospy.Time(options.end_time)
    except Exception as e:
        rospy.logfatal("failed to load bag file: %s", e)
        exit(1)
    finally:
        rospy.loginfo(f"loaded bag file: {fname}")

    try:
        for topic, msg, time in bag.read_messages(topics=options.topic_names,
                                                  start_time=stime,
                                                  end_time=etime):
            bag_out.write(topic, msg, time)
            
    except Exception as e:
        rospy.logwarn("fail: %s", e)
    finally:
        bag.close()
        bag_out.close()


def GetTopicList(path):
    bag = rosbag.Bag(path)
    topics = list(bag.get_type_and_topic_info()[1].keys())
    print(f"{topics=}")
    types = []
    for dict_values in list(bag.get_type_and_topic_info()[1].values()):
        print(dict_values[0])
        types.append(dict_values[0])

    results = []
    for to, ty in zip(topics, types):
        results.append(to)

    return results


def main(options):
    app = QtWidgets.QApplication(sys.argv)

    # GetFilePath
    files = []
    for i in range(options.bag_count):
        files.append(SimplePyQtGUIKit.GetFilePath(isApp=True, caption="Select bag file", filefilter="*bag"))
        print(f"{files=}")
    if len(files) < 1:
        print("Error:Please select a bag file")
        sys.exit()
    # topics = GetTopicList(files[0])
    # selected = SimplePyQtGUIKit.GetCheckButtonSelect(
    #     topics, app=app, msg="Select topics to be added")

    # options.topic_names = []
    # for k, v in selected.items():
    #     if v:
    #         options.topic_names.append(k)

    # if len(options.topic_names) == 0:
    #     print("Error:Please select topics")
    #     sys.exit()

    # options.output_file_format = "%t.csv"

    # print("Converting....")
    # for i in range(0, len(files) - 1):
    #     bag_to_csv(options, files[i])

    # QtWidgets.QMessageBox.information(
    #     QtWidgets.QWidget(),
    #     "Message", "Finish Convert!!")


if __name__ == '__main__':
    print("rosbag_to_rosbag start!!")
    print("waiting for roscore...")
    rospy.init_node('rosbag_to_rosbag', anonymous=True)
    parser = OptionParser(usage="%prog [options] bagfile")
    parser.add_option("-bag_count", "--bag_count", dest="bag_count",help="number of bagfile", type="int",default=2)
    (options, args) = parser.parse_args()

    main(options)
