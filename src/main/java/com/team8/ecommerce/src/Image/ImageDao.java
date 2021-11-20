package com.team8.ecommerce.src.Image;

import com.team8.ecommerce.src.Image.model.PostPredictReq;
import com.team8.ecommerce.src.Image.model.PostPredictRes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;
import javax.sql.DataSource;


@Repository
public class ImageDao {
    // *********************** 동작에 있어 필요한 요소들을 불러옵니다. **************************
    private JdbcTemplate jdbcTemplate;

    @Autowired
    public void setDataSource(DataSource dataSource){
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }
    // ***********************************************************************************

    // 이미지 저장
    public int saveImg(PostPredictReq postPredictReq){
        String saveImgQuery = "insert into Image (imgname, imgDir, imgClass) VALUES (?, ?, ?)";
        Object[] saveImgParams = new Object[]{
                postPredictReq.getImgname(),
                postPredictReq.getImagDir(),
                postPredictReq.getClass()};
        this.jdbcTemplate.update(saveImgQuery, saveImgParams);

        // 가장 마지막에 삽입된(생성된) idx값은 가져온다.
        String lastInsertIdxQuery = "select last_insert_id()";
        return this.jdbcTemplate.queryForObject(lastInsertIdxQuery, int.class);
    }
}