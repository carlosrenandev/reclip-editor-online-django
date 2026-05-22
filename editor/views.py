from pathlib import Path
import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from moviepy.video.io.VideoFileClip import VideoFileClip

def time_to_seconds(time_str):

    parts = time_str.split(":")

    if len(parts) != 2:
        raise ValueError("Formato inválido. Use mm:ss")

    minutes = int(parts[0])
    seconds = int(parts[1])

    return minutes * 60 + seconds


def home(request):
    video_url = None
    error = None

    if request.method == "POST":

        video = request.FILES.get("video")

        # Validar envio
        if not video:
            error = "Nenhum vídeo enviado."

            return render(
                request,
                "index.html",
                {
                    "error": error
                }
            )

        try:

            # Validar extensão
            valid_extensions = [
                ".mp4",
                ".avi",
                ".mov",
                ".mkv",
                ".flv",
                ".wmv",
                ".webm"
            ]

            file_ext = os.path.splitext(video.name)[1].lower()

            if file_ext not in valid_extensions:

                error = (
                    "Formato de vídeo não suportado. "
                    "Use MP4, AVI, MOV, MKV, FLV, WMV ou WEBM."
                )

                return render(
                    request,
                    "index.html",
                    {
                        "error": error
                    }
                )

            # Salvar vídeo original
            fs = FileSystemStorage()

            filename = fs.save(video.name, video)

            video_path = Path(fs.path(filename))

            # Obter dados do formulário
            start = time_to_seconds(request.POST.get("start", "0:00"))
            end = time_to_seconds(request.POST.get("end", "0:10"))

            remove_audio = request.POST.get("remove_audio") == "on"

            # Nome do vídeo final
            output_name = f"{uuid.uuid4()}.mp4"

            output_path = Path(settings.MEDIA_ROOT) / output_name

            # Criar pasta caso não exista
            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Abrir vídeo
            clip = VideoFileClip(str(video_path))

            # =========================
            # VALIDAR TEMPOS
            # =========================

            if start < 0:

                clip.close()

                error = "O tempo inicial não pode ser menor que 0."

                return render(
                    request,
                    "index.html",
                    {
                        "error": error
                    }
                )

            if end <= start:

                clip.close()

                error = (
                    "O tempo final deve ser maior "
                    "que o tempo inicial."
                )

                return render(
                    request,
                    "index.html",
                    {
                        "error": error
                    }
                )

            if end > clip.duration:

                clip.close()

                error = (
                    f"O tempo final não pode ser maior "
                    f"que a duração do vídeo"
                )

                return render(
                    request,
                    "index.html",
                    {
                        "error": error
                    }
                )

            # =========================
            # CORTAR VÍDEO
            # =========================

            clip = clip.subclipped(start, end)

            # Remover áudio
            if remove_audio:
                clip = clip.without_audio()

            # Exportar vídeo
            clip.write_videofile(
                str(output_path),
                codec="libx264",
                audio_codec="aac",
                logger=None
            )

            clip.close()

            # URL do vídeo processado
            video_url = f"{settings.MEDIA_URL}{output_name}"

            # Remover vídeo original
            try:
                video_path.unlink()

            except Exception:
                pass

            return render(
                request,
                "index.html",
                {
                    "video_url": video_url,
                    "error": None
                }
            )

        except Exception as e:

            error = f"Erro ao processar vídeo: {str(e)}"

            return render(
                request,
                "index.html",
                {
                    "error": error
                }
            )

    return render(
        request,
        "index.html",
        {
            "video_url": video_url,
            "error": error
        }
    )