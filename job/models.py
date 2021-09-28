import math
from datetime import datetime

from django.db import models


class JobField(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class JobAd(models.Model):
    advertiser = models.ForeignKey('employer.Employer', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True)
    expiration_date = models.DateField()
    job_fields = models.ManyToManyField(JobField, blank=True)
    description = models.TextField(blank=True)
    salary = models.IntegerField()
    work_hours_per_week = models.IntegerField()

    @staticmethod
    def get_unexpired_queryset():
        return JobAd.objects.filter(expiration_date__gte=datetime.today()).order_by('expiration_date')

    def get_common_applicant_job_fields(self, applicant_job_fields):
        ad_job_fields = self.job_fields.all()
        if not ad_job_fields:
            return 0
        return ad_job_fields.intersection(applicant_job_fields).count()

    @staticmethod
    def get_unexpired_queryset_with_common_job_fields_applicant(applicant):
        queryset = JobAd.get_unexpired_queryset()
        applicant_job_fields = applicant.job_fields.all()
        if not applicant_job_fields:
            return queryset
        queryset = sorted(queryset, key=lambda x: x.get_common_applicant_job_fields(applicant_job_fields), reverse=True)
        pks = [item.pk for item in queryset]
        queryset = JobAd.objects.filter(pk__in=pks)
        return queryset

    def __str__(self):
        return str(self.advertiser) + ' - ' + self.title

    def __repr__(self):
        return str(self.advertiser) + ' - ' + self.title

    class BinaryNode:

        def __init__(self, ad):
            self.ad = ad
            self.left = None
            self.right = None

    @staticmethod
    def __insert(node, ad):
        if node is None:
            return JobAd.BinaryNode(ad)
        if ad.salary >= node.ad.salary:
            node.right = JobAd.__insert(node.right, ad)
        elif ad.salary < node.value:
            node.left = JobAd.__insert(node.left, ad)
        return node

    @staticmethod
    def __get_binary_tree(queryset):
        root = None
        for ad in queryset:
            root = JobAd.__insert(root, ad)
        return root

    @staticmethod
    def __traverse_binary_tree(root, traversed, salary_min, salary_max):
        if root is None or root in traversed:
            return
        traversed.append(root)
        if not salary_min:
            JobAd.__traverse_binary_tree(root.left, traversed, salary_min, salary_max)
            if root.ad.salary <= salary_max:
                JobAd.__traverse_binary_tree(root.right, traversed, salary_min, salary_max)
                yield root.ad
        elif not salary_max:
            if salary_min <= root.ad.salary:
                JobAd.__traverse_binary_tree(root.left, traversed, salary_min, salary_max)
                yield root.ad
            JobAd.__traverse_binary_tree(root.right, traversed, salary_min, salary_max)
        else:
            if salary_min <= root.ad.salary:
                JobAd.__traverse_binary_tree(root.left, traversed, salary_min, salary_max)
            if salary_min <= root.ad.salary <= salary_max:
                yield root.ad
            if root.ad.salary <= salary_max:
                JobAd.__traverse_binary_tree(root.right, traversed, salary_min, salary_max)

    @staticmethod
    def get_queryset_by_salary(queryset, salary_min, salary_max):
        root = JobAd.__get_binary_tree(queryset)
        ads = []
        for ad in JobAd.__traverse_binary_tree(root, [], salary_min, salary_max):
            ads.append(ad.pk)
        return JobAd.objects.filter(pk__in=ads)

    def save(self, *args, **kwargs):
        pk = self.pk
        super().save(*args, **kwargs)
        if pk:
            JobAdSearch.objects.filter(ad__id=pk).delete()
        text = self.get_lemmatized_self()
        freq = {}
        for token in text:
            if token not in freq:
                freq[token] = 1
            else:
                freq[token] += 1
        total = len(text)
        for word in freq:
            freq[word] /= total
        indexes = []
        for word in freq:
            indexes.append(JobAdSearch(ad=self, word=word, index=freq[word]))
        JobAdSearch.objects.bulk_create(indexes)

    @staticmethod
    def search(queryset, text):
        text = set(JobAd.__get_lemmatized_text(text))
        ids = [item.id for item in queryset]
        if not ids:
            return JobAd.objects.none()
        N = len(ids)
        results = {}
        for token in text:
            indexes = JobAdSearch.objects.filter(ad__id__in=ids, word=token)
            idf = math.log(N / min(len(indexes) + 1, N))
            for index in indexes:
                tfidf = index.index * idf
                if index.ad.id not in results:
                    results[index.ad.id] = 0
                results[index.ad.id] += tfidf
        final_ids = sorted(results, key=lambda key: results[key], reverse=True)
        return JobAd.objects.filter(id__in=final_ids)

    def get_lemmatized_self(self):
        # stop_words = set(stopwords.words('english'))
        # title = [item for item in nltk.tokenize.word_tokenize(re.sub(r'[.!@#$%^&*()_+\']', '', self.title.lower()))
        #          if item not in stop_words]
        # description = [
        #     item for item in nltk.tokenize.word_tokenize(re.sub(r'[.!@#$%^&*()_+\']', '', self.description.lower()))
        #     if item not in stop_words]
        # job_fields = [
        #     [item for item in
        #      nltk.tokenize.word_tokenize(re.sub(r'[.!@#$%^&*()_+\']', '', field.name + ' ' + field.description)) if
        #      item not in stop_words] for field in self.job_fields.all()]
        # for item_list in job_fields:
        #     for item in item_list:
        #         description.append(item)
        # lemmatizer = WordNetLemmatizer()
        # title = [lemmatizer.lemmatize(item) for item in title]
        # description = [lemmatizer.lemmatize(item) for item in description]
        # return title + description
        return JobAd.__get_lemmatized_text(self.title) + JobAd.__get_lemmatized_text(self.description)

    @staticmethod
    def __get_lemmatized_text(text):
        return text.strip().lower().split()


class JobApplication(models.Model):
    applicant = models.ForeignKey('applicant.Applicant', on_delete=models.CASCADE)
    ad = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    description = models.TextField(blank=True)


class JobAdSearch(models.Model):
    ad = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)
    index = models.FloatField()
