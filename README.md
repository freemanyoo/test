# 이미지 → PDF 변환 도구

`image_to_pdf.py` 스크립트는 하나 이상의 이미지를 손쉽게 하나의 PDF로 묶어 줍니다. 폴더를 넘겨주면 내부에서 지원되는 확장자(`PNG`, `JPG`, `JPEG`, `BMP`, `TIFF`, `WEBP`)만 자동으로 추려 순서대로 합칩니다.

## 준비

```bash
pip install -r requirements.txt
```

## 사용 예시

```bash
# 개별 파일 지정
python image_to_pdf.py photo1.jpg photo2.png -o album.pdf

# 폴더 전체를 PDF 로
python image_to_pdf.py ./my_photos -o trip.pdf
```

변환이 끝나면 `총 N장의 이미지를 '.../output.pdf' PDF로 변환했습니다.` 메시지가 출력됩니다.
