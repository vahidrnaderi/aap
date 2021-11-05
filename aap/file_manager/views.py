"""File Manager views"""
import os
from django.conf import settings
from django.http import JsonResponse

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# from rest_framework import viewsets
from rest_framework.views import APIView
# from rest_framework.mixins import DestroyModelMixin
from rest_framework import permissions, generics, status
# from rest_framework.generics import GenericAPIView
# from django.http import HttpResponse, FileResponse
from rest_framework.response import Response


class FileManager(APIView):
    """File manager class"""
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_correct_path(self, path):
        if not path.startswith(str(self.request.user.id)):
            directory = os.path.join(str(self.request.user.id), path)
        else:
            directory = path
        directory_path = os.path.join(settings.MEDIA_ROOT, directory)
        return directory_path

    def create_path(self, path, new_folder):
        # Check if user root path dose not exist, create it.
        # if path:
        #     path = self.get_correct_path(path)
        # elif not path and :
        #     pass

        try:
            os.mkdir(os.path.join(path, new_folder))
        except FileExistsError:
            return Response(
                data={"status_code": status.HTTP_400_BAD_REQUEST,
                      "code": status.HTTP_400_BAD_REQUEST,
                      "detail": "Directory already existed!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return path

    def is_user_root(self, path):
        if not path.endswith('/aap/media/{0}'.format(self.request.user.id)) and \
           not path.endswith('/aap/media/{0}/'.format(self.request.user.id)):
            return True
        else:
            return False

    def post(self, request, url_path="", format=None):
        """Upload file or create directory."""
        if request.META['CONTENT_TYPE'] == 'application/json':
            """Create full url_path directory."""
            return JsonResponse({"directories": self.create_path(url_path, request.data['new_folder'])}, status=201)
        elif request.META['CONTENT_TYPE'].startswith('multipart/form-data'):
            """Upload file to url_path."""
            try:
                f = request.FILES['file']
            except FileNotFoundError:
                return Response(
                    data={"status_code": status.HTTP_400_BAD_REQUEST,
                          "code": status.HTTP_400_BAD_REQUEST,
                          "detail": "No file attached for upload."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            file_destination = os.path.join(self.create_path(url_path), f.name)
            with open(file_destination, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            return JsonResponse({"file_destination": file_destination}, status=201)
        else:
            return Response(
                data={"status_code": status.HTTP_400_BAD_REQUEST,
                      "code": status.HTTP_400_BAD_REQUEST,
                      "detail": "Unknown endpoint."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, url_path, format=None):
        """Delete file or directory"""
        path = self.get_correct_path(url_path)
        if os.path.isdir(path):
            """Delete directory."""
            if not self.is_user_root(path):
                try:
                    return Response(os.rmdir(path))  # {"Directory Deleted."})
                except FileNotFoundError:
                    # Directory dose not exist
                    return Response(
                        data={"status_code": status.HTTP_400_BAD_REQUEST,
                              "code": status.HTTP_400_BAD_REQUEST,
                              "detail": "Directory dose not exist!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except OSError:
                    # Directory is not empty
                    return Response(
                        data={"status_code": status.HTTP_400_BAD_REQUEST,
                              "code": status.HTTP_400_BAD_REQUEST,
                              "detail": "Directory is not empty!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    data={"status_code": status.HTTP_403_FORBIDDEN,
                          "code": status.HTTP_403_FORBIDDEN,
                          "detail": "This task is forbidden!"},
                    status=status.HTTP_403_FORBIDDEN
                )

        elif os.path.isfile(path):
            """Delete file."""
            try:
                return Response(os.remove(path))  # {"detail": "File Deleted."})
            except FileNotFoundError:
                # File dose not exist
                return Response(
                    data={"status_code": status.HTTP_400_BAD_REQUEST,
                          "code": status.HTTP_400_BAD_REQUEST,
                          "detail": "File dose not exist!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                    data={"status_code": status.HTTP_400_BAD_REQUEST,
                          "code": status.HTTP_400_BAD_REQUEST,
                          "detail": "Path is not correct!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

    def put(self, request, url_path, format=None):
        """
            Rename file/folder
            Copy file/folder
            Move file/folder
        """
        src = self.get_correct_path(url_path)
        dst = self.get_correct_path(url_path)

        if request.data.get("rename_to"):
            if not self.is_user_root(src):
                try:
                    return Response(os.rename(src, dst))
                except OSError:
                    return Response(
                        data={"status_code": status.HTTP_400_BAD_REQUEST,
                              "code": status.HTTP_400_BAD_REQUEST,
                              "detail": "Destination is a existed and not empty!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except IsADirectoryError:
                    return Response(
                        data={"status_code": status.HTTP_400_BAD_REQUEST,
                              "code": status.HTTP_400_BAD_REQUEST,
                              "detail": "Destination is a directory!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except NotADirectoryError:
                    return Response(
                        data={"status_code": status.HTTP_400_BAD_REQUEST,
                              "code": status.HTTP_400_BAD_REQUEST,
                              "detail": "Destination is a File!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        elif request.data.get("copy_to"):
            if not self.is_user_root(src):
                return Response({"copy"})
        elif request.data.get("move_to"):
            if not self.is_user_root(src):
                return Response({"move"})
        else:
            return Response(
                data={"status_code": status.HTTP_400_BAD_REQUEST,
                      "code": status.HTTP_400_BAD_REQUEST,
                      "detail": "Check your request data!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            return Response(os.rename(src, dst))
        except:
            return Response({"request": request.data})

    def get(self, request, url_path, format=None):
        print("get")
        print(request.data)
        print(url_path)
        return Response({"request": request.data})


# class FileUpload(APIView):
#     """File upload class"""
#     parser_classes = [MultiPartParser]
#
#     def post(self, request, format=None):
#
#         f = request.FILES['file']
#         file_destination = os.path.join(settings.MEDIA_ROOT, f.name)
#         with open(file_destination, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)
#         return JsonResponse({"file_destination": file_destination}, status=201)

        # newdoc = Document(docfile=f)
        # newdoc.save()


# class CreateDirectory(APIView):
#     """File upload class"""
#     parser_classes = [MultiPartParser]
#
#     def post(self, request, directory_name, format=None):
#         directory = os.path.join("user_directory", directory_name)
#         directory_path = os.path.join(settings.MEDIA_ROOT, directory)
#         try:
#             os.makedirs(directory_path)
#             return JsonResponse({"directory": directory_path}, status=201)
#         except FileExistsError:
#             return Response(data={"message": "Directory Existed!"}, status=status.HTTP_400_BAD_REQUEST)


# class RemoveDirectory(viewsets.ViewSet):
#     """File upload class"""
#     parser_classes = [MultiPartParser]
#
#     def destroy(self, request, directory_name, format=None):
#         directory = os.path.join("user_directory", directory_name)
#         directory_path = os.path.join(settings.MEDIA_ROOT, directory)
#         try:
#             os.remove(directory_path)
#             # return JsonResponse({"directory": directory_path}, status=201)
#         except FileExistsError:
#             return Response(data={"message": "Directory Existed!"}, status=status.HTTP_400_BAD_REQUEST)


# class RemoveDirectory(generics.DestroyAPIView):
#     """File upload class"""
#     parser_classes = [MultiPartParser]
#
#     def destroy(self, request, directory_name, format=None):
#         directory = os.path.join("user_directory", directory_name)
#         directory_path = os.path.join(settings.MEDIA_ROOT, directory)
#         try:
#             os.remove(directory_path)
#             # return JsonResponse({"directory": directory_path}, status=201)
#         except FileExistsError:
#             return Response(data={"message": "Directory Existed!"}, status=status.HTTP_400_BAD_REQUEST)


# class RemoveDirectory(APIView):
#     """File upload class"""
#     # parser_classes = [MultiPartParser]
#
#     def delete(self, request, directory_name, format=None):




# class RemoveDirectory(
#         DestroyModelMixin,
#         GenericAPIView):
#     """File upload class"""
#     # parser_classes = [MultiPartParser]
#
#     def destroy(self, request, directory_name, format=None):
#
#         print(request.method)
#         directory = os.path.join("user_directory", directory_name)
#         directory_path = os.path.join(settings.MEDIA_ROOT, directory)
#         try:
#             os.rmdir(directory_path)
#             # return JsonResponse({"directory": directory_path}, status=201)
#         except FileNotFoundError:
#             return Response(data={"message": "Directory Existed!"}, status=status.HTTP_400_BAD_REQUEST)
