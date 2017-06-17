import sqlite3
import pandas as pd

cnx=sqlite3.connect(r'C:\Users\sambhav\Desktop\winerama_2\winerama\db.sqlite3')
df=pd.read_sql_query("select * from reviews_finalbuy",cnx)

t=[]
d={}
		

def func1(pid):
	
	minsupport=20  #Both are in percent!
	minconf=20 

	for i in (range(len(df))):
		z=df['tranno'][i]
		if z not in t:
			t.append(z)
	

	no_of_tran=len(t)
	min_support=(minsupport*no_of_tran)/100	
	min_conf=minconf/100

	for item in t:
		f=0
		for i in (range(len(df))):
			if item==df['tranno'][i]:
				if f==0:	
					d[item]=[]
					f=1
				d[item].append(df['wine_id'][i])

	num=0
	for key in d:
		if pid in d[key]:
			num=num+1


	c1={}
	for key in d:
		for item in d[key]:
			if item not in c1: 
				c1[item]=1
			else:
				c1[item]=c1[item]+1
	l1={}
	for key in c1:
		if c1[key]>min_support:
			l1[key]=c1[key]

	
	c2={}
	if pid in l1:
		for item in l1:
			if item==pid:
				continue
			else:
				f=0
				for key in d:
					if item in d[key] and pid in d[key]:
						if f==0:
							c2[item]=1
							f=1
						else:
							c2[item]=c2[item]+1


	l2={}
	for key in c2:
		if c2[key]>min_support:
			l2[key]=c2[key]	


	c3={}
	ctr1=0
	for key in l2:
		ctr2=0
		for key1 in l2:
			if ctr2<ctr1:
				ctr2=ctr2+1
				continue
			if key==key1:
				continue
			else :
				ctr=0
				for key2 in d:
					if key in d[key2] and key1 in d[key2]:
						ctr=ctr+1
				if ctr != 0:
					temp=[]
					temp.append(key)
					temp.append(key1)
					temp=tuple(temp)
					c3[temp]=ctr
		ctr1=ctr1+1


	l3={}
	for key in c3:
		if c3[key]>min_support:
			l3[key]=c3[key]

	
	c4={}
	ctr1=0
	for key in l3:
		ctr2=0
		for key1 in l3:
			if ctr2<ctr1:
				ctr2=ctr2+1
				continue
			if key==key1:
				continue
			else :
				ctr=0
				for key2 in d:
					if key[0] in d[key2] and key1[0] in d[key2] and key[1] in d[key2] and key1[1] in d[key2]:
						ctr=ctr+1
				if ctr != 0:
					temp=[]
					temp=set(temp)
					temp.add(key[0])
					temp.add(key[1])
					temp.add(key1[0])
					temp.add(key1[1])
					temp=tuple(temp)
					c4[temp]=ctr
		ctr1=ctr1+1		

	l4={}
	for key in c4:
		if c4[key]>min_support:
			l4[key]=c4[key]	
	ans=0
	res=[]
	val=-1

	if bool(l4)==True:
		for key in l4:
			l4[key]=l4[key]/num
			#print(key,l4[key])
			if l4[key]>min_conf:
				ans=1
				if l4[key]>val:
					val=l4[key]
					res.append(key)
	
	if ans==0:
		if bool(l3)==True:
			for key in l3:
				l3[key]=l3[key]/num
				#print(key,l3[key])
				if l3[key]>min_conf:
					ans=1
					if l3[key]>val:
						val=l3[key]
						res.append(key)
	res1=[]
	for item in res:
		item=list(item)
		res1.append(item)

#	for item in res1:
#		print(item)


	return res1
#func1(112552)