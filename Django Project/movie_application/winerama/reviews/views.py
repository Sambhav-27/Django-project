from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Review, Wine, Cluster,Bought,FinalBuy
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, SearchForm
from .suggestions import update_clusters
import datetime
from .recommends import movie_suggestion
import pandas as pd
import sqlite3
from .apriori import func1

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def wine_list(request):
    wine_list = Wine.objects.order_by('-name')[300:700]
    context = {'wine_list':wine_list}
    return render(request, 'reviews/wine_list.html', context)


def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

def add_search(request): 
   
    if request.method == 'POST':
        if request.POST.get('numero', False):
            m = request.POST['numero']    
            print ("My Number is ", m )
            
            wine_list = Wine.objects.filter(name__contains=m)
            context = {'wine_list':wine_list}
            return render(request, 'reviews/searched_movies.html', context)

    
    return render(request, 'reviews/searched_movies.html')



@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,))) # after adding the review, it redirects to the same page again
    
   # return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    x = movie_suggestion(request.user.username)
    # wine_list = list(Wine.objects.filter(id__in=x))    
    wine_list = list(Wine.objects.filter(name__in=x))
    print("heretheycome", wine_list)
    # wine_list = x
    return render(request, 'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'wine_list': wine_list}
    )
    
 


@login_required
def shopping_cart(request):
    cnx = sqlite3.connect(r'C:\Users\sambhav\Desktop\winerama_2\winerama\db.sqlite3')
    df = pd.read_sql_query("select * from reviews_bought", cnx)
    user_name1 = request.user.username
    ad=[]
    for i in range(len(df)):
        if df['user_name'][i]== user_name1:
            wine_id=df['wine_id'][i]
            wine=Wine.objects.get(pk=wine_id)
            ad.append(wine)
    return render(request,'reviews/shopping_cart.html',{'movies':ad})    

@login_required
def add_movie(request, wine_id):
    cnx = sqlite3.connect(r'C:\Users\sambhav\Desktop\winerama_2\winerama\db.sqlite3')
    df = pd.read_sql_query("select * from reviews_bought", cnx)
    df1= pd.read_sql_query("select * from reviews_finalbuy",cnx)
    user_name1 = request.user.username
    t=[]
    t1=[]
    for i in range(len(df)):
        if df['user_name'][i]== user_name1:
            t.append(df['wine_id'][i])
    for i in range(len(df1)):
        if df1['user_name'][i]== user_name1:
            t1.append(df1['wine_id'][i])
    if int(wine_id) in t:
        return HttpResponseRedirect(reverse('reviews:already_added_to_cart', args=(wine_id,)))
    elif int(wine_id) in t1:
        return HttpResponseRedirect(reverse('reviews:already_bought', args=(wine_id,)))
    else:
        wine = get_object_or_404(Wine, pk=wine_id)
        buy = Bought()
        buy.wine = wine
        buy.user_name = user_name1
        buy.pub_date = datetime.datetime.now()
        buy.save()
        return HttpResponseRedirect(reverse('reviews:recently_bought', args=(wine.id,))) 



@login_required
def recently_bought(request,wine_id):
    wine=Wine.objects.get(pk=wine_id)
    res=func1(int(wine_id))
    r=len(res)
#    print(r)
 #   print(r-1)
    ans=[]
    ans1=[]
    if bool(res)==True:
        for item in res[r-1]:
            ans.append(item)
        for item in ans:
            wine1=Wine.objects.get(pk=item)
            ans1.append(wine1)
    return render(request,'reviews/recently_bought.html',{'wine':wine,'res':ans1}) 

@login_required
def already_bought(request,wine_id):
    wine=Wine.objects.get(pk=wine_id)
    return render(request,'reviews/already_bought.html',{'wine':wine}) 


@login_required
def already_added_to_cart(request,wine_id):
    wine=Wine.objects.get(pk=wine_id)
    return render(request,'reviews/already_added_to_cart.html',{'wine':wine}) 



@login_required
def checkout(request):
    cnx = sqlite3.connect(r'C:\Users\sambhav\Desktop\winerama_2\winerama\db.sqlite3')
    df = pd.read_sql_query("select * from reviews_bought", cnx)
    user_name1 = request.user.username
    t=[]
    tranno1=0
    df1=pd.read_sql_query("select * from reviews_finalbuy",cnx)
    for i in range(len(df1)):
        tranno1=df1['tranno'][i]
    for i in range(len(df)):
        if df['user_name'][i]==user_name1:
            wid=df['wine_id'][i]
            pid=df['id'][i]
            wine = get_object_or_404(Wine, pk=wid)
            t.append(df['wine_id'][i])
            buy=FinalBuy()
            buy.wine=wine
            buy.user_name=user_name1
            buy.buy_date=datetime.datetime.now()
            buy.tranno=tranno1+1
            buy.save()
            Bought.objects.filter(id=pid).delete()
    return render(request,'reviews/checkout.html') 


@login_required
def my_movies(request):
    cnx = sqlite3.connect(r'C:\Users\sambhav\Desktop\winerama_2\winerama\db.sqlite3')
    df = pd.read_sql_query("select * from reviews_finalbuy", cnx)
    user_name1 = request.user.username
    ad=[]
    for i in range(len(df)):
        if df['user_name'][i]== user_name1:
            wine_id=df['wine_id'][i]
            wine=Wine.objects.get(pk=wine_id)
            ad.append(wine)
    return render(request,'reviews/my_movies.html',{'movies':ad})    

@login_required
def remove_movie(request,wine_id):
    cnx = sqlite3.connect(r'C:\Users\sambhav\Desktop\winerama_2\winerama\db.sqlite3')
    df=pd.read_sql_query("select * from reviews_bought",cnx)
    user_name1=request.user.username
    for i in range(len(df)):
        if df['user_name'][i]==user_name1:
            if df['wine_id'][i]==int(wine_id):
                pid=df['id'][i]
                Bought.objects.filter(id=pid).delete()
    df=pd.read_sql_query("select * from reviews_bought",cnx)
    ad=[]
    for i in range(len(df)):
        if df['user_name'][i]== user_name1:
            wine_id=df['wine_id'][i]
            wine=Wine.objects.get(pk=wine_id)
            ad.append(wine)
    return render(request,'reviews/shopping_cart.html',{'movies':ad})    