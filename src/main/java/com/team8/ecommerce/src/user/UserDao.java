package com.team8.ecommerce.src.user;

import com.team8.ecommerce.src.user.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.List;

@Repository
public class UserDao {
    // *********************** 동작에 있어 필요한 요소들을 불러옵니다. *************************
    private JdbcTemplate jdbcTemplate;

    @Autowired
    public void setDataSource(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }
    // **********************************************************************************

    // 회원가입
    public int createUser(PostUserReq postUserReq) {
        String createUserQuery = "insert into User (username, nickname, email, password, phoneNum) VALUES (?,?,?,?,?)";
        Object[] createUserParams = new Object[]{
                postUserReq.getUsername(),
                postUserReq.getNickname(),
                postUserReq.getEmail(),
                postUserReq.getPassword(),
                postUserReq.getPhoneNum()};
        this.jdbcTemplate.update(createUserQuery, createUserParams);

        // 가장 마지막에 삽입된(생성된) idx값은 가져온다.
        String lastInsertIdxQuery = "select last_insert_id()";
        // 해당 쿼리문의 결과 마지막으로 삽인된 유저의 userIdx 반환
        return this.jdbcTemplate.queryForObject(lastInsertIdxQuery, int.class);
    }

    // 이메일 확인
    public int checkEmail(String email) {
        String checkEmailQuery = "select exists(select email from User where email = ?)";
        String checkEmailParams = email; // 해당(확인할) 이메일 값
        // checkEmailQuery, checkEmailParams를 통해 가져온 값(intgud)을 반환한다.
        // -> 쿼리문의 결과(존재하지 않음(False,0),존재함(True, 1))를 int형(0,1)으로 반환됩니다.
        return this.jdbcTemplate.queryForObject(checkEmailQuery, int.class, checkEmailParams);
    }

    // 닉네임 확인
    public int checkNickname(String nickname) {
        String checkNickNameQuery = "select exists(select nickname from User where nickname = ?)";
        String checkNicknameParams = nickname;
        return this.jdbcTemplate.queryForObject(checkNickNameQuery, int.class, checkNicknameParams);
    }

    // 로그인: 해당 email에 해당되는 user의 암호화된 비밀번호 값을 가져온다.
    public User getPwd(PostLoginReq postLoginReq) {
        String getPwdQuery = "select * from User where email = ?";
        // 주입될 email값을 클라이언트의 요청에서 주어진 정보를 통해 파라미터로 저장
        // queryForObject(쿼리, 자료형, 파라미터) 에 파라미터로 사용
        String getPwdParams = postLoginReq.getEmail();

        return this.jdbcTemplate.queryForObject(getPwdQuery,
                (rs, rowNum) -> new User(
                        rs.getInt("userIdx"),
                        rs.getString("username"),
                        rs.getString("nickname"),
                        rs.getString("email"),
                        rs.getString("password"),
                        rs.getString("phoneNum"),
                        rs.getInt("point"),
                        rs.getString("status")
                ),
                getPwdParams
        );
    }

    // 모든 사용자 정보 조회
    public List<GetUserRes> getUsers() {
        String getUsersQuery = "select * from User"; //User 테이블에 존재하는 모든 회원들의 정보를 조회하는 쿼리
        return this.jdbcTemplate.query(getUsersQuery,
                (rs, rowNum) -> new GetUserRes(
                        rs.getInt("userIdx"),
                        rs.getString("username"),
                        rs.getString("nickname"),
                        rs.getString("email"),
                        rs.getString("password"),
                        rs.getString("phoneNum"),
                        rs.getInt("point"),
                        rs.getString("status")
                )
        ); // 복수개의 회원정보들을 얻기 위해 jdbcTemplate 함수(Query, 객체 매핑 정보)의 결과 반환(동적쿼리가 아니므로 Parmas부분이 없음)
    }

    // 해당 nickname을 갖는 유저들의 정보 조회
    public List<GetUserRes> getUsersByNickname(String nickname) {
        String getUsersByNicknameQuery = "select * from User where nickname =?"; // 해당 이메일을 만족하는 유저를 조회하는 쿼리문
        String getUsersByNicknameParams = nickname;
        return this.jdbcTemplate.query(getUsersByNicknameQuery,
                (rs, rowNum) -> new GetUserRes(
                        rs.getInt("userIdx"),
                        rs.getString("username"),
                        rs.getString("nickname"),
                        rs.getString("email"),
                        rs.getString("password"),
                        rs.getString("phoneNum"),
                        rs.getInt("point"),
                        rs.getString("status")),
                getUsersByNicknameParams); // 해당 닉네임을 갖는 모든 User 정보를 얻기 위해 jdbcTemplate 함수(Query, 객체 매핑 정보, Params)의 결과 반환
    }

    // 해당 userIdx를 갖는 유저조회
    public GetUserRes getUser(int userIdx) {
        String getUserQuery = "select * from User where userIdx = ?"; // 해당 userIdx를 만족하는 유저를 조회하는 쿼리문
        int getUserParams = userIdx;
        return this.jdbcTemplate.queryForObject(getUserQuery,
                (rs, rowNum) -> new GetUserRes(
                        rs.getInt("userIdx"),
                        rs.getString("username"),
                        rs.getString("nickname"),
                        rs.getString("email"),
                        rs.getString("password"),
                        rs.getString("phoneNum"),
                        rs.getInt("point"),
                        rs.getString("status")),
                getUserParams); // 한 개의 회원정보를 얻기 위한 jdbcTemplate 함수(Query, 객체 매핑 정보, Params)의 결과 반환
    }

    // 회원 상태 변경
    public int modifyUserStatus(PatchUserStatusReq patchUserStatusReq) {
        String modifyUserStatusQuery = "update User set status = ? where userIdx = ? ";
        Object[] modifyUserStatusParams = new Object[]{patchUserStatusReq.getStatus(), patchUserStatusReq.getUserIdx()}; // 주입될 값들(nickname, userIdx) 순
        return this.jdbcTemplate.update(modifyUserStatusQuery, modifyUserStatusParams); // 대응시켜 매핑시켜 쿼리 요청(생성했으면 1, 실패했으면 0)
    }

    // 회원 포인트 적립
    public int saveUserPoint(PatchUserPointReq patchUserPointReq) {
        String modifyUserPointQuery = "update User set point = ? where userIdx = ? ";
        // 주입될 값들(point, userIdx) 순
        Object[] modifyUserPointParams = new Object[]{patchUserPointReq.getPoint(), patchUserPointReq.getUserIdx()};
        // 대응시켜 매핑시켜 쿼리 요청(생성했으면 1, 실패했으면 0)
        return this.jdbcTemplate.update(modifyUserPointQuery, modifyUserPointParams);
    }
}