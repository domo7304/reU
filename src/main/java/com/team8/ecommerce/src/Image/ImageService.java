package com.team8.ecommerce.src.Image;

import com.team8.ecommerce.config.BaseException;
import com.team8.ecommerce.src.Image.model.PostPredictReq;
import com.team8.ecommerce.src.Image.model.PostPredictRes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import static com.team8.ecommerce.config.BaseResponseStatus.DATABASE_ERROR;

@Service
public class ImageService {
    // *********************** 동작에 있어 필요한 요소들을 불러옵니다 ********************* //
    private final ImageDao imageDao;
    private final ImageProvider imageProvider;

    @Autowired
    public ImageService(ImageDao imageDao, ImageProvider imageProvider){
        this.imageDao = imageDao;
        this.imageProvider = imageProvider;
    }
    // ***************************************************************************** //

    // 추론 (POST)
    public int predicImg(PostPredictReq postPredictReq) throws BaseException{
        // 우선 추론 진행
        try{
            // 여기서 플라스크로 요청을 보내고 json으로 받아오는 작업 필요
        } catch (Exception exception){
            throw new BaseException(DATABASE_ERROR);
        }

        // 추론 완료 후 imgClass까지 받아왔다면 데이터베이스에 저장하고
        // 프론트 추후 작업을 위해 imgIdx 다시 보내주기
        try {
            int imgIdx = imageDao.saveImg(postPredictReq);
            return imgIdx;
        } catch (Exception exception){
            throw new BaseException(DATABASE_ERROR);
        }
    }
}
