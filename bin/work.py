
import os
from bin.control import Early_days

try:
    course_time = {}

    with open(os.getcwd() +"\\res\\time.csv","rb") as f:

        s = f.read().decode('gb2312').strip().split("\r\n")
       
        # print(s)
       
        for _ in s:

            时间段,开始时间,结束时间,节次 = _.split(",")
            course_time[节次] = (开始时间,结束时间)

        # print(course_time)

    course_attr = {}
    course_cnt = {}

    with open(os.getcwd() +"\\res\\course.csv","rb") as f:

        s = f.read().decode('gb2312').split("\r\n")

        cnt = 0
        for _ in s:
            
            cnt += 1
            if cnt == 1:continue

            课程,持续周,星期,时间段,开课链接 = _.split(",")
            周 = 持续周.strip("\"").split("|")
            
            # print(周)

            for i in 周:

                a, b = map(int, i.split("-"))
                for j in range(a, b+1):
                    c, d = map(int, 时间段.split("-"))
                    for k in range(c, d+1):
                        course_attr[(j, int(星期), k)]=(课程, 开课链接)
                        if 课程 in course_cnt: course_cnt[课程] += 1
                        else: course_cnt[课程] = 1

    # for it in course_attr:
    #     print(it, course_attr[it])

except Exception as e:

    import traceback
    traceback.print_exc()

course_dict = {}

def pt():

    print("课时统计")
    id = 0
    for it in course_cnt:
        
        id += 1
        course_dict[it] = id
        print("ID="+str(id),it,"总课时:"+str(course_cnt[it]))

# course_ID = 0 表示全部
# way_ID    = 1 查询当天课程
# way_ID    = 2 查询本周课程
def get_course(way_ID, course_ID):

    ret = []

    tmp = []

    for _ in course_attr:
        if course_ID == 0 or course_dict[course_attr[_][0]] == course_ID:
            tmp.append(_ + course_attr[_])
    tmp.sort()

    from datetime import date
    from datetime import datetime
    from datetime import timedelta

    now = datetime.now()

    if(Early_days != 0): now += timedelta(days = Early_days)

    print('当前时间为：' + now.strftime('%F') , now.strftime('%T'))

    now_w = (now.strftime("%W"),now.strftime("%w"))
    
    for _ in tmp:

        # datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        day = date(2020, 2, 23) + timedelta(days = (_[0]-1)*7+_[1])
        day_w = (day.strftime("%W"),day.strftime("%w"))

        # print(now_w, day_w)

        if now_w[0]==day_w[0] and (way_ID==2 and now_w[1]<=day_w[1] or way_ID==1 and now_w[1]==day_w[1]):
            ret.append(_)

    return ret

if __name__ == '__main__':
    pt()

    while 1:

        print("请输入查询方式ID：")
        print("\tID=1:查询当天课程")
        print("\tID=2:查询本周课程")

        y=input()
        while(y==""):y=input()

        y=int(y)

        if y<1 or y>2:
            continue

        tmp = get_course(y, 0)

        if len(tmp) == 0:
            print("今日" if y == 1 else "本周" + "无课程")

        tmp.sort()

        for _ in tmp:
            print("星期" + str(_[1]),"第"+str(_[2])+"节课",course_time[str(_[2])][0] + "-" + course_time[str(_[2])][1],_[3])


            
            # print("第"+str(_[0])+"周,"+"星期"+str(_[1])+",第"+str(_[2])+"节课")

        _ = input("回车以继续...")
