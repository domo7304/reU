package com.team8.ecommerce.src.Image;

import com.team8.ecommerce.config.BaseException;
import com.team8.ecommerce.config.BaseResponse;
import com.team8.ecommerce.src.Image.model.GetImgRes;
import com.team8.ecommerce.src.Image.model.PostPredictReq;
import com.team8.ecommerce.src.Image.model.PostPredictRes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;

@RestController
@RequestMapping("/app/images")
public class ImageController {
    // ************************ 동작에 있어 필요한 요소들을 불러옵니다. **************************
    @Autowired
    private final ImageProvider imageProvider;
    @Autowired
    private final ImageService imageService;
    @Autowired
    public ImageController(ImageProvider imageProvider, ImageService imageService){
        this.imageProvider = imageProvider;
        this.imageService = imageService;
    }
    // ************************************************************************************

    // 추론 API
    @PostMapping("/predict")
    public BaseResponse<PostPredictRes> predictImg(@RequestParam("file") MultipartFile file) throws IOException {
        String dir = "C:\\Users\\lee\\Desktop\\Laptop\\img\\";
        file.transferTo(new File(dir + file.getOriginalFilename()));
        try {
            PostPredictReq postPredictReq = new PostPredictReq(file.getOriginalFilename(), dir + file.getOriginalFilename(), "");
            PostPredictRes postPredictRes = imageService.predictImg(postPredictReq);
            return new BaseResponse<>(postPredictRes);
        } catch (BaseException exception){
            return new BaseResponse<>((exception.getStatus()));
        }
    }

    // path variable에 해당하는 이미지 조회 API
    @ResponseBody
    @GetMapping("/{imgIdx}")
    public BaseResponse<GetImgRes> getImages(@PathVariable("imgIdx") int imgIdx){
        try {
            GetImgRes getImgRes = imageProvider.getImg(imgIdx);
            return new BaseResponse<>(getImgRes);
        } catch (BaseException exception){
            return new BaseResponse<>((exception.getStatus()));
        }
    }
}
