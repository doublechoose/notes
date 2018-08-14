

```

public class BigDialog extends DialogFragment {


    public static BigDialog newInstance() {

        BigDialog dialog = new BigDialog();

        return dialog;
    }

    @NonNull
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        Dialog dialog = super.onCreateDialog(savedInstanceState);

        /*设置不带title*/
        dialog.getWindow().requestFeature(Window.FEATURE_NO_TITLE);
        return dialog;
    }


    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {

        /*设置背景透明*/
        getDialog().getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));

        View view = inflater.inflate(R.layout.big_dialog, container);

        ImageView closeBt = (ImageView) view.findViewById(R.id.img_close);

        closeBt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                dismiss();
            }
        });

        return view;
    }


}

```



```
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
              android:layout_width="wrap_content"
              android:layout_height="wrap_content"
              android:background="#00000000"
              android:orientation="vertical">

    <ImageView
        android:id="@+id/img_close"
        android:layout_width="18dp"
        android:layout_height="18dp"
        android:layout_gravity="right"
        android:background="@drawable/big__close"
        android:src="@drawable/big_close"/>
    <LinearLayout
        android:orientation="vertical"
        android:layout_marginTop="5dp"
        android:paddingTop="16dp"
        android:paddingLeft="15dp"
        android:paddingRight="15dp"
        android:paddingBottom="17dp"

        android:background="@drawable/big_dialog_bg"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content">

        <TextView
            android:id="@+id/img_content"
            android:layout_width="315dp"
            android:layout_height="wrap_content"
            android:text="@string/big_info"
            />
    </LinearLayout>

</LinearLayout>
```
