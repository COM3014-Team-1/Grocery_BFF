import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.stereotype.Service;

@Service
public class ProductService {

    @Autowired
    private ProductHandler productHandler;

    public Page<Product> getAllProducts(int page, int size) {
        return productHandler.getProducts(page, size);  // delegate to handler
    }

    public Product getProductById(Long id) {
        return productHandler.getProductById(id);  // delegate to handler
    }
}
