package com.team8.ecommerce.src.user;

import com.team8.ecommerce.config.BaseException;
import com.team8.ecommerce.config.BaseResponse;
import com.team8.ecommerce.src.user.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

import static com.team8.ecommerce.config.BaseResponseStatus.*;
import static com.team8.ecommerce.src.utils.ValidationRegex.*;

@RestController
@RequestMapping("/app/users")
public class UserController {
    // *********************** 동작에 있어 필요한 요소들을 불러옵니다. *************************
    @Autowired
    private final UserProvider userProvider;
    @Autowired
    private final UserService userService;
    @Autowired

    public UserController(UserProvider userProvider, UserService userService) {
        this.userProvider = userProvider;
        this.userService = userService;
    }
    // ******************************************************************************

    // 회원가입 API
    @ResponseBody
    @PostMapping("/sign-up")
    public BaseResponse<PostUserRes> createUser(@RequestBody PostUserReq postUserReq) {

        // 사용자 이름 공백 확인
        if (postUserReq.getUsername() == null || postUserReq.getUsername() == "") {
            return new BaseResponse<>(POST_USERS_EMPTY_USERNAME);
        }
        // 사용자 닉네임 공백 확인
        if (postUserReq.getNickname() == null || postUserReq.getNickname() == "") {
            return new BaseResponse<>(POST_USERS_EMPTY_NICKNAME);
        }
        // 사용자 이메일 공백 확인
        if (postUserReq.getEmail() == null || postUserReq.getEmail() == "") {
            return new BaseResponse<>(POST_USERS_EMPTY_EMAIL);
        }
        // 사용자 이메일  형식 확인
        if (!isRegexEmail(postUserReq.getEmail())) {
            return new BaseResponse<>(POST_USERS_INVALID_EMAIL);
        }
        // 사용자 비밀번호 공백 확인
        if (postUserReq.getPassword() == null || postUserReq.getPassword() == "") {
            return new BaseResponse<>(POST_USERS_EMPTY_PASSWORD);
        }
        // 사용자 비밀번호 형식 확인
        if (!isRegexPassword(postUserReq.getPassword())) {
            return new BaseResponse<>(POST_USERS_INVALID_PASSWORD);
        }
        // 휴대폰 번호 공백 확인
        if (postUserReq.getPhoneNum() == null || postUserReq.getPhoneNum() == "") {
            return new BaseResponse<>(POST_USERS_EMPTY_PHONE);
        }
        // 휴대폰 번호 형식 확인
        if (!isRegexPhone(postUserReq.getPhoneNum())) {
            return new BaseResponse<>(POST_USERS_INVALID_PHONE);
        }
        // 사용자 저장
        try {
            PostUserRes postUserRes = userService.createUser(postUserReq);
            return new BaseResponse<>(postUserRes);
        } catch (BaseException exception) {
            return new BaseResponse<>((exception.getStatus()));
        }
    }

    @ResponseBody
    @PostMapping("/log-in")
    public BaseResponse<PostLoginRes> logIn(@RequestBody PostLoginReq postLoginReq) {
        // 사용자 이메일 공백 확인
        if (postLoginReq.getEmail() == null || postLoginReq.getEmail() == "") {
            return new BaseResponse<>(POST_USERS_EMPTY_EMAIL);
        }
        // 사용자 이메일  형식 확인
        if (!isRegexEmail(postLoginReq.getEmail())) {
            return new BaseResponse<>(POST_USERS_INVALID_EMAIL);
        }
        // 사용자 비밀번호 공백 확인
        if (postLoginReq.getPassword() == null || postLoginReq.getPassword() == "") {
            return new BaseResponse<>(POST_USERS_EMPTY_PASSWORD);
        }
        // 로그인 시도
        try {
            PostLoginRes postLoginRes = userProvider.logIn(postLoginReq);
            return new BaseResponse<>(postLoginRes);
        } catch (BaseException exception) {
            return new BaseResponse<>(exception.getStatus());
        }
    }

    @ResponseBody
    @GetMapping("") //Query String 방식으로 가져오기
    //  @RequestParam은, 1개의 HTTP Request 파라미터를 받을 수 있는 어노테이션(?뒤의 값).
    //  default로 RequestParam은 반드시 값이 존재해야 하도록 설정되어 있지만, (전송 안되면 400 Error 유발)
    //  required 설정으로 필수 값에서 제외 시킬 수 있음
    //  defaultValue를 통해, 기본값(파라미터가 없는 경우, 해당 파라미터의 기본값 설정)을 지정할 수 있음
    public BaseResponse<List<GetUserRes>> getUsers(@RequestParam(required = false) String nickname) {
        try {
            // query string인 nickname이 없을 경우, 그냥 전체 유저정보를 불러온다.
            if (nickname == null) {
                List<GetUserRes> getUsersRes = userProvider.getUsers();
                return new BaseResponse<>(getUsersRes);
            }
            // query string인 nickname이 있을 경우, 조건을 만족하는 유저정보들을 불러온다.
            List<GetUserRes> getUsersRes = userProvider.getUsersByNickname(nickname);
            return new BaseResponse<>(getUsersRes);
        } catch (BaseException exception) {
            return new BaseResponse<>((exception.getStatus()));
        }
    }

    @ResponseBody // Path-variable 방식으로 가져오기
    @GetMapping("/{userId}") // (GET) 127.0.0.1:9000/app/users/:userId
    public BaseResponse<GetUserRes> getUser(@PathVariable("userId") int userId) {
        // @PathVariable RESTful(URL)에서 명시된 파라미터({})를 받는 어노테이션, 이 경우 userId값을 받아옴.
        //  null값 or 공백값이 들어가는 경우는 적용하지 말 것
        try {
            GetUserRes getUserRes = userProvider.getUser(userId);
            return new BaseResponse<>(getUserRes);
        } catch (BaseException exception) {
            return new BaseResponse<>((exception.getStatus()));
        }
    }

    @ResponseBody
    @PatchMapping("/userStatus")
    public BaseResponse<String> modifyUserStatus(@RequestBody PatchUserStatusReq patchUserStatusReq) {
        try {
            userService.modifyUserStatus(patchUserStatusReq);
            String result = "회원 상태가 수정되었습니다.";
            return new BaseResponse<>(result);
        } catch (BaseException exception) {
            return new BaseResponse<>((exception.getStatus()));
        }
    }

    @ResponseBody
    @PatchMapping("/point")
    public BaseResponse<String> modifyUserName(@RequestBody PatchUserPointReq patchUserPointReq) {
        try {
            userService.saveUserPoint(patchUserPointReq);
            String result = "회원 포인트가 적립되었습니다.";
            return new BaseResponse<>(result);
        } catch (BaseException exception) {
            return new BaseResponse<>((exception.getStatus()));
        }
    }
}