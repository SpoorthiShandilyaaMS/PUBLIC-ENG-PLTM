from django.shortcuts import render,redirect
from appdb.models import User
from appdb.models import Constituency
from appdb.models import News_Feed
from appdb.models import Complaint
from appdb.models import Sector
from appdb.models import Query
from appdb.models import Answer
from django.http import HttpResponse
import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import TransactionManagementError
from django.contrib.auth.models import auth
from django.contrib import messages
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.utils import timezone
import logging

# function for homepage view
def home_view(request):
    return render(request, 'appdb/home.html')




# function for getting data from sigunup form
@csrf_exempt
def get_signup_data(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        pwd = request.POST.get('user_password')
        mobile = request.POST.get('user_mobile')
        constituency =request.POST.get('user_constituency')

        if(name and email and pwd and constituency):

            # get id of the constituency
            const_id = get_object_or_404(Constituency,constituency_name=constituency).constituency

            # save the record into users table
            try:
                if not User.objects.filter(uemail=email).exists():
                    if not User.objects.filter(username=name).exists():
                        reg = User(const_id=const_id,username=name,uemail=email,upassword=pwd,umobile=mobile,uconsname=constituency,usertype='public')
                        regstatus = reg.save()
                        # send HttpResponse
                        responseData = {
                            'code': 200,
                            'message': 'Successfully registered',
                            'data' :{
                               'user_email': email,
                               'user_name' : name,
                               'constituency_id': const_id,
                               'constituency_name': constituency
                            }
                        }
                    else:
                        # send HttpResponse
                        responseData = {
                            'code': 400,
                            'message': 'This Username has already been taken',
                        }
                     # return redirect('login')
                        return JsonResponse(responseData)
                else:
                    # send HttpResponse
                    responseData = {
                        'code': 400,
                        'message': 'This Email has already been registered',
                    }
                    return JsonResponse(responseData)
            except Exception as e:
                # log the exceptions
                responseData = {
                    'code': 500,
                    'message': 'Something went wrong!!'+str(e),
                }
                return JsonResponse(responseData)
        else:
            responseData = {
                'code': 400,
                'message': 'No input field can be empty!!!!',
            }
            return JsonResponse(responseData)

    else:
        return render(request,'appdb/signupp.html')



# function for validating data from login form
@csrf_exempt
def login(request):
    if request.method =='POST':
        email = request.POST.get('user_email')
        pwd = request.POST.get('user_password')
        type = request.POST.get('type')

        # if email and pwd not null
        if(email and pwd):
            #if user email exists
            try:
                if User.objects.filter(uemail=email).exists():
                    # if useremail exists and the password matches
                    if User.objects.filter(uemail=email).filter(upassword=pwd).exists():
                        userData = User.objects.filter(uemail=email).values('uemail','uconsname','const_id','username','usertype')
                        responseData={
                            'code': 200,
                            'message': 'login Successful',
                            'user_Data' : list(userData),
                        }
                    else:
                        # email exists but corresponding password is incorrect
                        responseData = {
                            'code': 400,
                            'message': 'Incorrect Password',
                        }
                else:
                    # the given email doesnt exists
                    responseData = {
                        'code': 400,
                        'message': 'No user with '+email+' exists.Check email entered!!',
                    }
                return JsonResponse(responseData, safe=False)
            except:
                # log the exceptions
                responseData = {
                    'code': 500,
                    'message': 'Something went wrong!!',
                }
                return JsonResponse(responseData, safe=False)
        else:
            # responsedata if no email pwd found
            responseData = {
                'code': 400,
                'message': 'Please Enter proper credentials!!',
            }
        return JsonResponse(responseData, safe=False)

    else:
        return render(request,'appdb/login.html')



@csrf_exempt
def add_feed(request):
    if request.method=='POST':
        newstitle = request.POST.get('news_title')
        newsdesc = request.POST.get('news_description')
        constituencyname = request.POST.get('constituency_name')



        if(newstitle and newsdesc and constituencyname):


            const_id = get_object_or_404(Constituency,constituency_name=constituencyname).constituency
            # return HttpResponse(const_id)
            try:
                reg = News_Feed(feed_title=newstitle,feed_description=newsdesc,constituency_name=constituencyname,constituency_id=const_id)
                regstatus = reg.save()
                responseData = {
                    'code': 200,
                    'message': 'Successfully added news feed',
                    }
                return JsonResponse(responseData)

            except Exception:
                responseData = {
                    'code': 500,
                    'message': 'something went wrong!!',
                }
                return JsonResponse(responseData)
        else:
            responseData = {
                'code': 400,
                'message': 'Please Enter proper Feeds!!',
            }
            return JsonResponse(responseData)






@csrf_exempt
def get_all_feeds(request):
    if request.method == 'GET':
        const_id=request.GET['const_id']

        if(const_id):
            try:
                if News_Feed.objects.filter(constituency_id = const_id).exists():
                    userData = News_Feed.objects.filter(constituency_id = const_id).order_by('-id').values('id','constituency_name','feed_title','feed_description','feed_date')
                    responseData ={
                    'code' : 200,
                    'msg' : 'successfully news shown',
                    'data' : list(userData),
                    }
                    return JsonResponse(responseData, safe=False)
                else:
                    responseData ={
                    'code' : 400,
                    'msg' : 'No feeds to show'
                    }
                    return JsonResponse(responseData, safe=False)

            except Exception as e:
                responseData = {
                    'code': 500,
                    'message': 'Something went wrong!!',
                }
                return JsonResponse(responseData, safe=False)

        else:
            responseData ={
            'code' : 400,
            'msg' : 'Specify Constituency ID'
            }
            return JsonResponse(responseData, safe=False)





@csrf_exempt
def edit_feed(request):
    if request.method=='POST':
        feedid = request.POST.get('feed_id')
        newstitle = request.POST.get('news_title')
        newsdesc = request.POST.get('news_description')




        if(newstitle and newsdesc and feedid):

            try:
                updateRes = News_Feed.objects.filter(id=feedid).update(feed_title=newstitle,feed_description=newsdesc)

                responseData = {
                    'code': 200,
                    'feed_id':feedid,
                    'newstitle':newstitle,
                    'newsdesc':newsdesc,
                    'message': 'Successfully edited news feed',
                    }
                return JsonResponse(responseData)

            except Exception as e :
                responseData = {
                    'code': 500,
                    'message': str(e),
                }
                return JsonResponse(responseData)
        else:
            responseData = {
                'code': 400,
                'message': 'Please provide proper Feed details!!',
            }
            return JsonResponse(responseData)





@csrf_exempt
def delete_feed(request):
    if request.method=='POST':
        feedid = request.POST.get('feed_id')

        if(feedid):
            try:
                if News_Feed.objects.filter(id=feedid).exists():
                    delres = News_Feed.objects.filter(id=feedid).delete()

                    responseData = {
                    'code': 200,
                    'feed_id':feedid,
                    'message': 'Successfully deleted news feed',
                    }
                    return JsonResponse(responseData)
                else:
                    responseData = {
                    'code': 400,
                    'message': 'No feed with id '+feedid,
                    }
                    return JsonResponse(responseData)


            except Exception as e:
                responseData = {
                    'code': 500,
                    'message': str(e),
                }
                return JsonResponse(responseData)

        else:
            responseData = {
                'code': 400,
                'message': 'Please provide feed id!!',
            }
            return JsonResponse(responseData)



@csrf_exempt
def add_complaint(request):
    if request.method=='POST':

        compsub = request.POST.get('complaint_subject')
        compdetails = request.POST.get('complaint_details')
        sectorname =  request.POST.get('sector_name')
        constname = request.POST.get('constituency_name')
        postedbyname =  request.POST.get('posted_by_name')

        if(compsub and compdetails and sectorname and postedbyname and constname):

            sectorid = get_object_or_404(Sector,sector_name=sectorname).sector_id
            # get id of the constituency
            const_id = get_object_or_404(Constituency,constituency_name=constname).constituency

            try:
                reg = Complaint(complaint_subject=compsub,complaint_details=compdetails,posted_by_name=postedbyname,const_id=const_id,const_name=constname,sector_name=sectorname,sector_id=sectorid)
                regstatus = reg.save()
                responseData = {
                    'code': 200,
                    'message': 'Successfully complaint registered'
                }
                return JsonResponse(responseData)

            except Exception as e:
                responseData = {
                    'code': 500,
                    'message': str(e),
                }
                return JsonResponse(responseData)


        else:
            responseData = {
                'code': 400,
                'message': 'Enter all complaint feilds',
            }
            return JsonResponse(responseData)


@csrf_exempt
def upvote(request):
    if request.method=='POST':

        complaintid = request.POST.get('complaint_id')
        username = request.POST.get('user_name')

        if(complaintid and username):

            try:
                complaint = get_object_or_404(Complaint,id=complaintid)
                upvotedby = complaint.upvoted_by
                noofupvotes = complaint.no_up_vote

                if not upvotedby:
                    upvoted = Complaint.objects.filter(id=complaintid).update(upvoted_by=username,no_up_vote=noofupvotes+1)
                else :
                    upvotedusers = upvotedby.split('~')
                    if username in upvotedusers:
                        responseData = {
                            'code': 200,
                            'message': 'This user has already upvoted the isuue..'
                        }
                        return JsonResponse(responseData)

                    upvotedby = upvotedby + '~' + username
                    upvoted = Complaint.objects.filter(id=complaintid).update(upvoted_by=upvotedby,no_up_vote=noofupvotes+1)

                if upvoted:
                    responseData = {
                        'code': 200,
                        'message': 'Successfully upvoted'
                    }
                    return JsonResponse(responseData)


            except Exception as e:
                responseData = {
                    'code': 500,
                    'message': str(e),
                }
                return JsonResponse(responseData)


        else:
            responseData = {
                'code': 400,
                'message': 'Enter all details(complaint id and username)',
            }
            return JsonResponse(responseData)

@csrf_exempt
def get_all_complaints(request):
    if request.method == 'GET':
        const_id=request.GET['const_id']

        if(const_id):
            try:
                if Complaint.objects.filter(const_id = const_id).exists():
                    complaintData = Complaint.objects.filter(const_id = const_id).order_by('id').values('id','complaint_subject','complaint_details','const','sector','sector_name','posted_by_name','const_name','upvoted_by','no_up_vote')
                    responseData ={
                    'code' : 200,
                    'msg' : 'successfully complaints shown',
                    'data' : list(complaintData),
                    }
                    return JsonResponse(responseData, safe=False)
                else:
                    responseData ={
                    'code' : 400,
                    'msg' : 'No complaints to show'
                    }
                    return JsonResponse(responseData, safe=False)

            except Exception as e:
                responseData = {
                    'code': 500,
                    'message': 'Something went wrong!!',
                }
                return JsonResponse(responseData, safe=False)

        else:
            responseData ={
            'code' : 400,
            'msg' : 'Specify Constituency ID'
            }
            return JsonResponse(responseData, safe=False)

@csrf_exempt
def add_query(request):
    if request.method=='POST':
        query = request.POST.get('query')
        postedbyname = request.POST.get('posted_by_name')
        qconstname = request.POST.get('qconst_name')

        if(query and postedbyname and qconstname):

            const_id = get_object_or_404(Constituency,constituency_name=qconstname).constituency



            try:
                reg = Query(query=query,posted_by_name=postedbyname,qconst_id=const_id,qconst_name=qconstname)
                regstatus = reg.save()
                responseData = {
                    'code': 200,
                    'message': 'Successfully added query',
                    }
                return JsonResponse(responseData)

            except Exception as e:
                responseData = {
                    'code': 500,
                    'message': 'something went wrong!!'+str(e),
                }
                return JsonResponse(responseData)
        else:
            responseData = {
                'code': 400,
                'message': 'Please Enter proper query details!!',
            }
            return JsonResponse(responseData)

@csrf_exempt
def get_all_queries(request):
    if request.method == 'GET':
        const_id=request.GET['const_id']

        if(const_id):
            try:
                if Query.objects.filter(qconst_id = const_id).exists():
                    userData = Query.objects.filter(qconst_id = const_id).order_by('id').values('id','query','posted_by_name','qconst_id','qconst_name','date','answered_by')

                    responseData ={
                    'code' : 200,
                    'msg' : 'successfully queries shown',
                    'data' : list(userData),
                    }
                    return JsonResponse(responseData, safe=False)
                else:
                    responseData ={
                    'code' : 400,
                    'msg' : 'No queries to show'
                    }
                    return JsonResponse(responseData, safe=False)

            except Exception as e:
                responseData = {
                    'code': 500,
                    'message': 'Something went wrong!!'+str(e),
                }
                return JsonResponse(responseData, safe=False)

        else:
            responseData ={
            'code' : 400,
            'msg' : 'Specify Constituency ID'
            }
            return JsonResponse(responseData, safe=False)

@csrf_exempt
def add_answer(request):
    if request.method=='POST':
        answer = request.POST.get('answer')
        username = request.POST.get('answered_by_name')
        queryid = request.POST.get('query_id')

        if(answer and username and queryid):
            # queryid = get_object_or_404(Query,query=queryname).id


            try:
                answeredBy = get_object_or_404(Query,id=queryid).answered_by

                # update in Query table
                if not answeredBy:
                    answeredByUserAdd = Query.objects.filter(id=queryid).update(answered_by=username)
                else :
                    answeredUsers = answeredBy.split('~')

                    if username in answeredUsers:
                        responseData = {
                            'code': 200,
                            'message': 'This user has already answered this query...'
                        }
                        return JsonResponse(responseData)
                    else:
                        answeredUsers = answeredBy + '~' + username
                        answered = Query.objects.filter(id=queryid).update(answered_by=answeredUsers)

                answerres = Answer(answer=answer,answered_by_name=username,query_id=queryid)
                regstatus = answerres.save()
                responseData = {
                    'code': 200,
                    'message': 'Successfully added answer',
                    }
                return JsonResponse(responseData)

            except Exception as e:
                responseData = {
                    'code': 500,
                    'message': 'something went wrong!!'+str(e),
                }
                return JsonResponse(responseData)
        else:
            responseData = {
                'code': 400,
                'message': 'Please Enter proper fields!!',
            }
            return JsonResponse(responseData)






# @csrf_exempt
# def get_all_query_answers(request):
#     if request.method == 'GET':
#         constid=request.GET.get('const_id')
#         if(constid):
#             try:
#                 queryData = Query.objects.filter(qconst_id=constid).values('id','query','posted_by_name','qconst_id','qconst_name','answered_by')
#                 queryData = list(queryData)
#
#                 for query in queryData:
#                     return HttpResponse(query.id)
#                 return HttpResponse(len(queryData))
#                     # answerData = Answer.objects.order_by('id').values('id','answer','answered_by_name','query_id','date')
#                 responseData ={
#                     'code' : 200,
#                     'msg' : 'successfully queries shown',
#                     'data' : list(answerData),
#                     }
#                 return JsonResponse(responseData, safe=False)
#             except Exception as e:
#                 responseData = {
#                     'code': 500,
#                     'message': 'Something went wrong!!'+str(e),
#                 }
#                 return JsonResponse(responseData, safe=False)
#
#         else:
#             responseData ={
#             'code' : 400,
#             'msg' : 'Specify query ID'
#             }
#             return JsonResponse(responseData, safe=False)
