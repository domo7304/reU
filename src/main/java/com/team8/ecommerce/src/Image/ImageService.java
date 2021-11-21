package com.team8.ecommerce.src.Image;

import com.team8.ecommerce.config.BaseException;
import com.team8.ecommerce.src.Image.model.PostPredictReq;
import com.team8.ecommerce.src.Image.model.PostPredictRes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;


import static com.team8.ecommerce.config.BaseResponseStatus.DATABASE_ERROR;
import static com.team8.ecommerce.config.BaseResponseStatus.SERVER_ERROR;

@Service
public class ImageService {
    // *********************** 동작에 있어 필요한 요소들을 불러옵니다 ********************* //
    private final ImageDao imageDao;

    @Autowired
    public ImageService(ImageDao imageDao){
        this.imageDao = imageDao;
    }
    // ***************************************************************************** //

    // 추론 (POST)
    public PostPredictRes predictImg(PostPredictReq postPredictReq) throws BaseException{
        // 우선 추론 진행
        RestTemplate restTemplate = new RestTemplate();
        postPredictReq = restTemplate.postForObject("http://localhost:5000/fileUpload", postPredictReq, PostPredictReq.class);

        // 추론 완료 후 imgClass 값까지 저장하여 postPredictReq DTO 다 채웠으면 데이터베이스에 저장하고
        // 프론트 추후 작업을 위해 imgIdx 다시 보내주기
        try {
            int imgIdx = imageDao.saveImg(postPredictReq);
            return new PostPredictRes(imgIdx);
        } catch (Exception exception){
            // throw new BaseException(DATABASE_ERROR);
            throw new BaseException(SERVER_ERROR);
        }
    }
}
