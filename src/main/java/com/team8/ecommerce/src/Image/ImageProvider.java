package com.team8.ecommerce.src.Image;

import com.team8.ecommerce.config.BaseException;
import com.team8.ecommerce.src.Image.model.GetImgRes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import static com.team8.ecommerce.config.BaseResponseStatus.DATABASE_ERROR;
import static com.team8.ecommerce.config.BaseResponseStatus.SERVER_ERROR;

@Service
public class ImageProvider {
    // *********************** 동작에 있어 필요한 요소들을 불러옵니다 *************************
    private final ImageDao imageDao;

    @Autowired
    public ImageProvider(ImageDao imageDao){
        this.imageDao = imageDao;
    }
    // *********************************************************************************

    // 해당 imgIdx를 갖는 img의 정보 조회
    public GetImgRes getImg(int imgIdx) throws BaseException{
        try {
            GetImgRes getImgRes = imageDao.getImg(imgIdx);
            return getImgRes;
        } catch (Exception exception){
            // throw  new BaseException(DATABASE_ERROR);
            throw new BaseException(SERVER_ERROR); // 어디서 에러나는지 확인하게 여기는 서버에러로 대체
        }
    }
}
