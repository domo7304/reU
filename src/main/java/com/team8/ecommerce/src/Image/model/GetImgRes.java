package com.team8.ecommerce.src.Image.model;

import lombok.*;

@Getter // 해당 클래스에 대한 접근자 생성
@Setter // 해당 클래스에 대한 설정자 생성
@AllArgsConstructor
public class GetImgRes {
    private int imgIdx;
    private String imgname;
    private String imgDir;
    private String imgClass;
    private String status;
}
