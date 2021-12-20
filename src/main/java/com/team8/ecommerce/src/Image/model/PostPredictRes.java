package com.team8.ecommerce.src.Image.model;

import lombok.*;

@Getter
@Setter
@AllArgsConstructor
public class PostPredictRes {
    private int imgIdx;
    private String imgname;
    private String imgDir;
    private String imgClass;
    private String status;
}
