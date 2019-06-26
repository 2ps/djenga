# Secrets management

Secrets management in config files is not hard, it's just complicated.
We want our apps to be easily deployable using CI/CD, but that can't
be done unles the secrets are either (1) made part of the CI/CD process,
like by entering values into a UI that is stored by a CI/CD service like
Wercker or VSTS, (2) made part of the repository itself, or (3) held in a 
secure storage for access via api like hashicorp vault.  If we want
secrets to live inside of a repository, we further have to make sure
they are encrypted.  

CAVEATS:  Whichever system you pick does have trade-offs
in terms of ease of use, security, and cost of implementation.  kms wrapped
decryption can be very slow, for example, compared to known-key symmetric
decryption, since it requires initialization of boto3 as well as the 
decryption operation which is an API call to aws services.  

In order to facilitate (2), djenga provides some okay (not great) primitives 
for secrets management using aws kms key wrapping.  To be sure, using
aws is necessary for this type of secrets management.  Developers can
encrypt secrets using the command line kms_wrap utility

        kms_wrap --key my_awesome_key --region=us-west-2
        Enter plaintext: my secret
        
        
And the kms_wrap utility will output a secret like:

        AQIDAHjoDoY5jTiEMti6GvnxgaUmSScPWHLIJfOeuut12UzGWwH6WkTzc
        j4yWXdCpUZWlgchAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSI
        b3DQEHATAeBglghkgBZQMEAS4wEQQMq3aOCYcJgCVPI0G8AgEQgDt4ZpG
        k52qeuCvYeYJOLB3A4wThIfgyU+bBJdLXBDuTvaQq3ZYJlwEkmZujd4mX
        vU/xOGtU0IaK2BeZAg==|sBHP0wx51rl1/Xw=|A0Y00M5auR41Wuxf2Xh
        Hxg==|QXyNIko+Ph6Ra+zulww0Og==|HmYqCKyQV57uBMBWq+ORTwF++m
        uslTygVDgHdwG+Bko=
 
that you can then paste in as a value in a config file.  That secret
can either be decrypted at run time using 
`djenga.encryption.kms_wrapped.decrypt`


