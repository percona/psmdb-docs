## Check encryption status

You can check the encryption status and the current configuration using the following command:

```{.javascript data-prompt=">"}
> db.serverStatus().encryptionAtRest
```

??? example "Expected output"

    ```{.text .no-copy}
    {
      encryptionEnabled: true,
      encryptionCipherMode: 'AES256-CBC',
      encryptionKeyId: 'local'
    }
    ```