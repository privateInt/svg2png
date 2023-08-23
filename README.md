# svg2png

## 목적
- 이미지 파일을 작게 resize하는 경우, 이미지 손실을 줄이기위해 svg파일로 변환 후 png로 변환합니다.
- 속도를 높이기위해 중간 resize 과정이 있습니다.

## 작업결과
- 이미지를 input으로 받아 svg 및 png 파일을 각각 생성합니다.

## 환경설정
- pip install -r requirements.txt

## arguments
- src-path: 변환 대상이 되는 이미지들의 디렉토리 path입니다. (ex. '/home/ubuntu/workspace/dataset/test_dataset_svg/spec69_src')
- dst-path: 작업 결과 이미지들이 저장되는 디렉토리 path입니다. (ex. '/home/ubuntu/workspace/dataset/test_dataset_svg/seunghoon_test')
- size-for-resize: svg 및 png 변환전 속도를 높이기 위한 중간 resize과정의 이미지 크기 설정입니다.
- size-for-png: 최종적으로 저장되는 이미지 크기 설정입니다.
- remove-svg: 작업 중간에 생성되는 svg파일을 삭제할지 여부입니다.
- multi-thread-num: 멀티쓰레드 갯수입니다.

## 사용예시
- cd [your workspace]
- python MultiThread_svg_final.py --remove-svg True
