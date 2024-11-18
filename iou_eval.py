import os

#针对yolov8不同检测的结果进行比对

#原图宽和高
width=1920
height=1080

#iou匹配限制
strict=0.8

#推理结果
inf_dir='/home/ustc/multi/labels'

#对照结果
eval_dir='/home/ustc/multi/eval'

#自动读取inf_dir内的文件名然后与eval_dir中的对应文件进行匹配
#文件夹里最好全都是.txt
files=os.listdir(inf_dir)

#每张图的值
everyf1=[]

#每张图的对象数量
inf_num=[]

#每张图的对象box平均大小
inf_size=[]

for file in files:

    inf_texts=[]
    eval_texts=[]
    tp=0
    fp=0
    tn=0
    fn=0
    f1score=0
    number=0
    sum = 0
    iou=0

    tbox=[]
    sum_size=0
    
    #逐个读推理结果
    inf_path=os.path.join(inf_dir,file)
    with open(inf_path,'r') as inf:
        inf_txt=inf.readlines()

    #找到对应的文件名相同的对照结果
    eval_path=os.path.join(eval_dir,file)
    with open(eval_path,'r') as eval:
        eval_txt=eval.readlines()



    #将读入的字符串列表转化成数组
    for line1 in inf_txt:
        elements = []
        elements = line1.split(' ')
        elements = list(map(float, elements))
        elements[0] = int(elements[0])

        inf_texts.append(elements)

    for line2 in eval_txt:
        elements = []
        elements = line2.split(' ')
        elements = list(map(float, elements))
        elements[0] = int(elements[0])

        eval_texts.append(elements)

    #对象数量
    tlen=len(inf_texts)
    rlen=len(eval_texts)

    if inf_texts[0][0]==0:
        inf_num.append(0)
    else:
        inf_num.append(tlen)

    #每次取一行进行比对
    for itext in inf_texts:

        tleft=itext[1]*width
        ttop=itext[2]*height
        twid=itext[3]*width
        thei=itext[4]*height

        #计算对象box平均大小
        tsize=twid*thei
        tbox.append(tsize)

        for etext in eval_texts:
            rleft=etext[1]*width
            rtop=etext[2]*height
            rwid=etext[3]*width
            rhei=etext[4]*height

            #计算IOU
            area_a = twid * thei
            area_b = rwid * rhei

            w = min(rleft+rwid,tleft+twid) - max(tleft,rleft)
            h = min(rtop+rhei,ttop+thei) - max(ttop,rtop)

            if w <= 0 or h <= 0:
                iou=0
            else:
                area_c = w * h
                iou=area_c / (area_a + area_b - area_c)

            if(iou>=strict): #匹配位置
                tp+=1  #都对的上为TP
            #else: 
                #fp+=1  #标签对不上为FP

        #如果当前对象没有匹配项,且标签值不为0，则记为FP    
        if(tp==0 and fp==0 and itext[0]!=0):
            fp+=1

    if(tlen>=rlen):
        fp=fp+(tlen-rlen) #样本比标准多也是FP
    else:
        fn=fn+(rlen-tlen) #样本比标准少是FN

    if(tp == 0 and fp == 0):
         p=0
    else:
         p=tp/(tp+fp)

    if(tp == 0 and fn == 0):
         r=0
    else:
         r=tp/(tp+fn)

    if((p == 0) & (r == 0)):
         f1score = 0
    else:
        f1score=(2*p*r)/(p+r)
    everyf1.append(f1score)
    for i in range(0,len(tbox)):
        sum_size=sum_size+int(tbox[i])
    inf_size.append(int(sum_size/len(tbox)))
    number = number + 1

#输出f1值
for i in range(0,len(everyf1)):
    print(everyf1[i])


#输出每张图的物体数量
for i in range(0,len(inf_num)):
    print(inf_num[i])


#输出每张图的物体平均box
for i in range(0,len(inf_size)):
    print(inf_size[i])



    

