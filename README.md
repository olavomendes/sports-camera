# SPORTS CAMERA

Sistema para captura contínua de frames de câmera com buffer circular e gravação do trecho recente acionada por comando serial.

## Requisitos
- Python 3.8 ou superior
- Bibliotecas Python: `opencv-python`, `pyserial`, `imageio`, `imageio-ffmpeg`

## Instalação
Instale as dependências:

```bash
pip install opencv-python pyserial imageio imageio-ffmpeg
```

## Testar a câmera
Teste rápido da câmera:

```bash
python -c "import cv2; cap=cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'ERROR')"
```

Se imprimir "ERROR", tente índices 1 ou 2.

## Execução
Execute o script principal:

```bash
python sports-camera.py
```

O script inicia a captura e mantém um buffer circular em memória.

## Como funciona
- O script inicia a captura em `CAMERA_SOURCE` (câmera local ou IP) e guarda frames em um buffer de duração `BUFFER_SECONDS`.
- Ao receber o comando serial `SAVE` ou `SALVAR`, o script salva os frames do buffer em um arquivo MP4.
- Os arquivos são salvos na pasta definida por `OUTPUT_FOLDER` (padrão `records`).

## Configuração
Ajuste os parâmetros no início de [sports-camera.py](sports-camera.py#L1-L200):
- `CAMERA_SOURCE`: índice da câmera local (0, 1, ...) ou URL para câmera IP (ex.: `"rtsp://192.168.1.10:554/stream"`)
- `BUFFER_SECONDS`: segundos mantidos no buffer
- `FPS`: quadros por segundo
- `SERIAL_PORT`: porta serial (ex.: COM3)
- `RESOLUTION`: resolução (largura, altura)
- `OUTPUT_FOLDER`: pasta de saída
- `CAMERA_TIMEOUT`: timeout em segundos para conexão com câmera IP

## Câmeras IP
Para usar uma câmera IP, altere `CAMERA_SOURCE` no arquivo:

```python
# Exemplo: câmera IP via RTSP
CAMERA_SOURCE = "rtsp://192.168.1.10:554/stream"
```

O script reconhecerá automaticamente se é uma câmera local ou IP e ajustará o comportamento:
- Câmeras IP: tentará reconectar até 5 vezes se a conexão cair
- Câmeras locais: funcionam como antes

## Solução de problemas
- Se a câmera não abrir, verifique o índice e os drivers.
- Se a porta serial não abrir, confirme a porta e feche outros programas que usam a porta serial.
- Se ocorrer erro ao salvar vídeo, instale o ffmpeg ou `imageio-ffmpeg`.
