package com.team8.ecommerce.src.Image;

import com.team8.ecommerce.src.Image.model.GetImgRes;
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
    public PostPredictRes saveImg(PostPredictReq postPredictReq){
        String saveImgQuery = "insert into Image (imgname, imgDir, imgClass) VALUES (?, ?, ?)";
        Object[] saveImgParams = new Object[]{
                postPredictReq.getImgname(),
                postPredictReq.getImgDir(),
                postPredictReq.getImgClass()};
        this.jdbcTemplate.update(saveImgQuery, saveImgParams);

        // 가장 마지막에 삽입된(생성된) idx값은 가져온다.
        String lastInsertIdxQuery = "select * from Image where imgIdx = last_insert_id()";
        return this.jdbcTemplate.queryForObject(lastInsertIdxQuery,
                (rs, rowNum) -> new PostPredictRes(
                        rs.getInt("imgIdx"),
                        rs.getString("imgname"),
                        rs.getString("imgDir"),
                        rs.getString("imgClass"),
                        rs.getString("status"))
                );
    }

    // 해당 imgIdx를 갖는 이미지 조회
    public GetImgRes getImg(int imgIdx){
        String getImgQuery = "select * from Image where imgIdx = ?";
        int getImgParams = imgIdx;
        return this.jdbcTemplate.queryForObject(getImgQuery,
                (rs, rowNum) -> new GetImgRes(
                        rs.getInt("imgIdx"),
                        rs.getString("imgname"),
                        rs.getString("imgDir"),
                        rs.getString("imgClass"),
                        rs.getString("status")),
                getImgParams);
    }
}
