package com.team8.ecommerce.src.user;

import com.team8.ecommerce.config.BaseException;
import com.team8.ecommerce.config.secret.Secret;
import com.team8.ecommerce.src.user.model.*;
import com.team8.ecommerce.src.utils.AES128;
import com.team8.ecommerce.src.user.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

import static com.team8.ecommerce.config.BaseResponseStatus.*;

@Service
public class UserProvider {
    // *********************** 동작에 있어 필요한 요소들을 불러옵니다 *************************
    private final UserDao userDao;

    @Autowired
    public UserProvider(UserDao userDao) {
        this.userDao = userDao;
    }
    // *********************************************************************************


    // 로그인(password 검사)
    public PostLoginRes logIn(PostLoginReq postLoginReq) throws BaseException {
        User user = userDao.getPwd(postLoginReq);
        String password;
        try {
            password = new AES128(Secret.USER_INFO_PASSWORD_KEY).decrypt(user.getPassword()); // 암호화
            // 회원가입할 때 비밀번호가 암호화되어 저장되었기 떄문에 로그인을 할때도 암호화된 값끼리 비교를 해야합니다.
        } catch (Exception ignored) {
            throw new BaseException(PASSWORD_DECRYPTION_ERROR);
        }
        //비밀번호가 일치한다면 userIdx를 return
        if (postLoginReq.getPassword().equals(password)) {
            return new PostLoginRes(user.getUserIdx());
        } else { // 비밀번호가 다르다면 에러메세지를 출력한다.
            throw new BaseException(FAILED_TO_LOGIN);
        }
    }

    // 해당 이메일이 이미 User Table에 존재하는지 확인
    public int checkEmail(String email) throws BaseException {
        try {
            return userDao.checkEmail(email);
        } catch (Exception exception) {
            throw new BaseException(DATABASE_ERROR);
        }
    }

    // 해당 닉네임이 이미 User Table에 존재하는지 확인
    public int checkNickname(String nickname) throws BaseException {
        try {
            return userDao.checkNickname(nickname);
        } catch (Exception exception) {
            throw new BaseException(DATABASE_ERROR);
        }
    }

    // User들의 정보를 조회
    public List<GetUserRes> getUsers() throws BaseException {
        try {
            List<GetUserRes> getUserRes = userDao.getUsers();
            return getUserRes;
        } catch (Exception exception) {
            throw new BaseException(DATABASE_ERROR);
        }
    }

    // 해당 nickname을 갖는 User들의 정보 조회
    public List<GetUserRes> getUsersByNickname(String nickname) throws BaseException {
        try {
            List<GetUserRes> getUsersRes = userDao.getUsersByNickname(nickname);
            return getUsersRes;
        } catch (Exception exception) {
            throw new BaseException(DATABASE_ERROR);
        }
    }

    // 해당 userIdx를 갖는 User의 정보 조회
    public GetUserRes getUser(int userIdx) throws BaseException {
        try {
            GetUserRes getUserRes = userDao.getUser(userIdx);
            return getUserRes;
        } catch (Exception exception) {
            throw new BaseException(DATABASE_ERROR);
        }
    }
}