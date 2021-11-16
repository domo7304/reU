package com.team8.ecommerce.src.user.model;

import lombok.*;

@Getter // 해당 클래스에 대한 접근자 생성
@Setter // 해당 클래스에 대한 설정자 생성
@AllArgsConstructor
public class PatchUserStatusReq {
    private int userId;
    private String state;
}
