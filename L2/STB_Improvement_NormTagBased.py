
import random
import math
import operator
import os

class NormTagBased():
    def __init__(self,fileName):
        self.fileName=fileName
        self.loadData()
        self.randomlySplitData(0.2)
        self.initStat()
        self.testRecommend()

    def loadData(self):
        print("Load Data\n")
        fileName=self.fileName
        self.records={}
        fi = open(fileName)
        lineNum=0
        for line in fi:
            lineNum+=1
            if lineNum ==1:
                continue
            uid,iid,tag,timestamp=line.split('\t')
            uid=int(uid)-1
            iid=int(iid)-1
            tag=int(tag)-1
            self.records.setdefault(uid,{})
            self.records[uid].setdefault(iid,[])
            self.records[uid][iid].append(tag)
        fi.close()
        print("Data Size %d"%(lineNum))
        print("Set tag userNumber %d"%(len(self.records)))
        print("Data loaded\n")

    def randomlySplitData(self,ratio,seed=100):
        random.seed(seed)
        self.train=dict()
        self.test=dict()
        for u in self.records.keys():
            for i in self.records[u].keys():
                if random.random()<ratio:
                    self.test.setdefault(u,{})
                    self.test[u].setdefault(i,[])
                    for t in self.records[u][i]:
                        self.test[u][i].append(t)
                else:
                    self.train.setdefault(u,{})
                    self.train[u].setdefault(i,[])
                    for t in self.records[u][i]:
                        self.train[u][i].append(t)
        print("Train sets Num %d ,Test sets Num %d"%(len(self.train),len(self.test)))

    def initStat(self):
        records=self.train
        self.user_tags=dict()
        self.tag_items=dict()
        self.user_items=dict()
        self.tag_users=dict()
        for u,items in records.items():
            for i,tags in items.items():
                for tag in tags:
                    self._addValueToMat(self.user_tags,u,tag,1)
                    self._addValueToMat(self.tag_items,tag,i,1)
                    self._addValueToMat(self.user_items,u,i,1)
                    self._addValueToMat(self.tag_users,tag,u,1)
        print("Initialized \n")
        print("user_tag: %d tag_items: %d user_items: %d  tag_users: %d"%(len(self.user_tags),len(self.tag_items),len(self.user_items),len(self.tag_users)))

    def _addValueToMat(self,mat,index,item,value=1):
        if index not in mat:
            mat.setdefault(index,{})
            mat[index].setdefault(item,value)

        else:
            if item not in mat[index]:
                mat[index][item]=value
            else:
                mat[index][item]+=value

    def precisionAndRecall(self,N):
        hit=0
        h_recall=0
        h_precision=0
        for user,items in self.test.items():
            if user not in self.train:
                continue
            rank=self.recommend(user,N)
            for item,rui in rank:
                if item in items:
                    hit+=1
            h_recall+=len(items)
            h_precision+=N
        return (hit/(h_precision*1.0)),(hit/(h_recall*1.0))


    def recommend(self,user,N):
        recommend_items=dict()
        tagged_items = self.user_items[user]
        for tag ,wut in self.user_tags[user].items():# wut =user_tags
            for item ,wti in self.tag_items[tag].items():#wti = tag_items
                if item in tagged_items:
                    continue
                if item not in recommend_items:
                    recommend_items[item]=(wut/len(self.user_tags[user])) * (wti/len(self.tag_items[tag]))
                else:
                    recommend_items[item]+=(wut/len(self.user_tags[user])) * (wti/len(self.tag_items[tag]))

        return sorted(recommend_items.items(),key=operator.itemgetter(1),reverse=True)[0:N]

    def testRecommend(self):
        print("Evaluation of Recommendation results\n")
        print("%3s %10s %10s"%('N',"precision","recallrate"))
        for n in [5,10,20,40,60,80,100]:
        # for n in [5,10]:
            precision,recall=self.precisionAndRecall(n)
            print("%3d %10.3f%% %10.3f%%" % (n, precision * 100, recall * 100))

if __name__ == '__main__':
    ntb=NormTagBased("./user_taggedbookmarks-timestamps.dat")


'''
用户打标签记录： records[i] = {user, item, tag}
用户打过的标签：user_tags[u][t] 
用户打过标签的商品：user_items[u][i]
打上某标签的商品：tag_items[t][i]
某标签使用过的用户：tags_users[t][u]

'''




