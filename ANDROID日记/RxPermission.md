android M版本需要动态申请危险权限，按照原生的写法，特别麻烦，需要覆盖`onRequestPermissionsResult`,写一堆东西。用RxPermission可以减少代码量。

```java
public void onClick(View v) {
    if(v == this) {
        if(this.mAttachActionListener == null || !this.mAttachActionListener.onAttachItemClick(this, this.mFavorite)) {
            PermissionUtil.clickWithPermission(v.getContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE, new PermissionUtil.DealEvent() {
                @Override
                public void deal() {
                    AttachAudioView.this.onAttachItemClick();

                }
            });
        }
        return;
    }
}
```

PermissionUtil.java

```java
public class PermissionUtil {

    private PermissionUtil(){}

    public static void clickWithPermission(final Context context, final String permission, final DealEvent dealEvent){

        RxPermissions.getInstance(context).request(permission)
                .subscribe(new Action1<Boolean>() {
                    @Override
                    public void call(Boolean grant) {
                        if (grant) {
                            /*有权限，继续执行*/
                            dealEvent.deal();
                        } else {
                            /*没有权限，显示无权限toast*/
                            ToastUtils.display(context, "您没有授权该权限，请在设置中打开权限");
                        }
                    }
                });
    }

    public interface DealEvent {
        void deal();
    }
}
```

这么写就可以将代码量减少一些了。

## 源码

RxPermission源码很少，只有三个类：

- Permission
- RxPermissions
- RxPermissionsFragment

就是通过写好的设置动态申请权限的Fragment去申请权限，来达到效果。









