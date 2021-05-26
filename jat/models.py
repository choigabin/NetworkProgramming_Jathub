from django.db import models

#데이터베이스 테이블 구조

class Repository(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200) #여기까지가 레퍼지토리의 필수 요소
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #repo1.introduction_set 나와 연결되어 있는 introduction의 set을 가져옴
    # repo1.introduction_all 나와 연결되어 있는 자소서를 전부 가져옴

    def __str__(self):
        return self.name

class Introduction(models.Model):
    # Repository테이블에 있는 애랑 Introduction 테이블에 있는 애랑 repository라는 내용으로 연결
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE) #intro1.repository 내 자소서가 속한 회사 이름
    # 1:n의 관계에서 n에게 Foreignkey를 사용
    version = models.IntegerField(default=1)
    contents = models.TextField()
    #intro1.comment_set 자기 속성이 없어도 닷을 붙이면 자기랑 연결되어있는 애들 값 가져올 수 있음

    def __str__(self):
        return f'{self.version} {self.contents}'

class Comment(models.Model):
    introduction = models.ForeignKey(Introduction, on_delete=models.CASCADE) #comment1.introduction
    comment = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


