package com.team8.ecommerce.src.Image;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ImageProvider {
    // *********************** 동작에 있어 필요한 요소들을 불러옵니다 *************************
    private final ImageDao imageDao;

    @Autowired
    public ImageProvider(ImageDao imageDao){
        this.imageDao = imageDao;
    }
    // *********************************************************************************


}
