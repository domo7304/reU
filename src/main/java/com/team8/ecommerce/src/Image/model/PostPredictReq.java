package com.team8.ecommerce.src.Image.model;

import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class PostPredictReq {
    private String imgname;
    private String imgDir;
    private String imgClass;
}
